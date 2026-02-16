import json
import csv
from datetime import datetime
import os
import pandas as pd
import glob

def create_stats(lega):
    lega_safe = lega.replace(" ", "_")
    base_path = os.path.join("csv", lega_safe)
    input_csv = os.path.join(base_path, f"{lega_safe}.csv")
    output_csv = os.path.join(base_path, "Statistiche_Somma_Gol.csv")

    #Elimino vecchi file se esistenti
    if os.path.exists(output_csv):
        os.remove(output_csv)


    # Leggo il file .csv
    df = pd.read_csv(input_csv)

    # Converto 'Somma Gol' in numerico (gestisce anche valori non numerici)
    df['Somma Gol'] = pd.to_numeric(df['Somma Gol'], errors='coerce')
    df['Gol Casa'] = pd.to_numeric(df['Gol Casa'], errors='coerce')
    df['Gol Trasferta'] = pd.to_numeric(df['Gol Trasferta'], errors='coerce')

    # Rimuovo eventuali partite non valide
    df = df.dropna(subset=['Somma Gol', 'Gol Casa', 'Gol Trasferta'])

    #Dataset gol totali
    df_all = df.copy()

    # Filtro solo le partite con somma gol >= 3
    partite_over3 = df[df['Somma Gol'] >= 3]

    # Conto quante volte ogni squadra appare (sia casa che trasferta)
    casa_over = partite_over3['Squadra Casa'].value_counts()
    trasferta_over = partite_over3['Squadra Trasferta'].value_counts()
    partite_over = casa_over.add(trasferta_over, fill_value=0).astype(int)

    # Calcolo gol fatti e subiti per ogni squadra
    gol_fatti_casa = df_all.groupby('Squadra Casa')['Gol Casa'].sum()
    gol_subiti_casa = df_all.groupby('Squadra Casa')['Gol Trasferta'].sum()
    gol_fatti_trasferta = df_all.groupby('Squadra Trasferta')['Gol Trasferta'].sum()
    gol_subiti_trasferta = df_all.groupby('Squadra Trasferta')['Gol Casa'].sum()
    
    # Sommo gol fatti e subiti totali
    gol_fatti = gol_fatti_casa.add(gol_fatti_trasferta,fill_value=0).astype(int)
    gol_subiti = gol_subiti_casa.add(gol_subiti_trasferta,fill_value=0).astype(int)

    # Creo il dataframe finale
    risultato = pd.DataFrame({
        'Nome Squadra': partite_over.index,
        'Partite con Somma Gol >= 3': partite_over.values,
        'Gol Fatti': gol_fatti.reindex(partite_over.index, fill_value=0).values,
        'Gol Subiti': gol_subiti.reindex(partite_over.index, fill_value=0).values
    })

    # Ordino
    risultato = risultato.sort_values('Partite con Somma Gol >= 3', ascending=False).reset_index(drop=True)

    # Salvo
    risultato.to_csv(output_csv, index=False)


def clean_merge_data(lega):

    lega_safe = lega.replace(" ", "_")

    base_path = os.path.join("csv", lega_safe)
    output_csv = os.path.join(base_path, f"{lega_safe}.csv")

    #Elimino vecchi file se esistenti
    if os.path.exists(output_csv):
        os.remove(output_csv)

    # creo array vuoto per concatenare file
    dfs = []
    filenames = glob.glob(os.path.join(base_path, "*_giornata_*.csv"))

    # leggo tutti i file nella lista
    for filename in filenames:
        dfs.append(pd.read_csv(filename, sep=","))

    # concateno i file
    lega_df = pd.concat(dfs, ignore_index=True)

    # seleziono e riordino solo le colonne che mi interessano
    lega_df = lega_df[
        ['Squadra Casa', 'Squadra Trasferta', 'Gol Casa', 'Gol Trasferta']
    ]
    lega_df['Somma Gol'] = lega_df['Gol Casa'] + lega_df['Gol Trasferta']
    # salvo in csv
    lega_df.to_csv(output_csv, index=False)
    create_stats(lega)



def create_csv_from_json_files():
    
    # Usa la cartella dove si trova lo script, non la directory di esecuzione
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Mostra tutti i file JSON nella cartella
    all_files = [f for f in os.listdir('.') if f.endswith('.json')]

    
    files_processed = 0
    
    #Itero tutti i file json che ho
    for round_num in range(1, 39):  
        filename = f'round_{round_num}.json'
        
        if not os.path.exists(filename):
            continue
        
        try:            
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'events' not in data or len(data['events']) == 0:
                print("Nessun evento trovato")
                continue

            lega = data['events'][0]['tournament']['name']

            #creo cartella lega
            csv_folder = os.path.join('csv', lega.replace(" ", "_"))
            os.makedirs(csv_folder, exist_ok=True)

            #creo file csv per ogni giornata
            csv_filename = os.path.join(
                csv_folder,
                f"{lega.replace(' ', '_')}_giornata_{round_num}.csv"
            )

            #riempio con i dati
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Data', 'Ora', 'Squadra Casa', 'Squadra Trasferta', 'Gol Casa', 'Gol Trasferta', 'Stato']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for match in data['events']:
                    home_team = match.get('homeTeam', {}).get('name', 'Sconosciuto')
                    away_team = match.get('awayTeam', {}).get('name', 'Sconosciuto')
                    home_score = match.get('homeScore', {}).get('current', '-')
                    away_score = match.get('awayScore', {}).get('current', '-')
                    status = match.get('status', {}).get('description', 'Sconosciuto')
                    if status == 'Postponed':
                        continue
                    timestamp = match.get('startTimestamp', 0)
                    match_date = datetime.fromtimestamp(timestamp)
                    
                    writer.writerow({
                        'Data': match_date.strftime('%d/%m/%Y'),
                        'Ora': match_date.strftime('%H:%M'),
                        'Squadra Casa': home_team,
                        'Squadra Trasferta': away_team,
                        'Gol Casa': home_score,
                        'Gol Trasferta': away_score,
                        'Stato': status
                    })
            files_processed += 1

            clean_merge_data(lega)

        except json.JSONDecodeError:
            print(f"❌ Errore nel file JSON")
        except Exception as e:
            print(f"❌ Errore: {e}")


if __name__ == "__main__":
    create_csv_from_json_files()
    