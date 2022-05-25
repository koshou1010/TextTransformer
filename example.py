import os 
import utils


def make_folder(): 
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)    


if __name__ == '__main__':
    INPUT_FOLDER = 'data'
    OUTPUT_FOLDER = 'data_t'
    make_folder()
    txtrtf = utils.TextTransformerType1(OUTPUT_FOLDER)  
    for root, dirs, files in os.walk(INPUT_FOLDER):
        for file in files:
            if file.endswith('txt'):
                txtrtf.entrance(root+'\\'+file)