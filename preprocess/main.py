from preprocess import Preprocess

def main():
    # Preprocess().get_vocabulary('/home/rebeca/crawler-bbc/filters/duplasBoas.csv')
    # Preprocess().preprocess('/home/rebeca/crawler-bbc/filters/duplasBoas.csv')
    # Preprocess().get_length('/home/rebeca/crawler-bbc/preprocess/duplasBoas_pp.csv')
    Preprocess().get_graph('/home/rebeca/crawler-bbc/preprocess/LenSubtitles.csv')
    
        
if __name__ == '__main__':
    main()

""" soma acumulada titulo:  814024
soma acumulada subtitulo:  4455402
média titulo:  10925.176824276263
média subtítulo:  59796.82991316485
"""