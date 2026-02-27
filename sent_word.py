
import glob# Step 2: Specify the directory containing your text files.

import numpy as np
    

import os
import glob
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

data_dir = 'Text/'
IDX = []
# Step 3: Use glob to find all text files in the directory.
file_paths = glob.glob(os.path.join(data_dir, '*.txt'))


arr = []
for iii in range(0,len(file_paths)):
    arr.append(int(file_paths[iii][5:len(file_paths[iii])-4]))
    
for ele in sorted(file_paths):
	print(ele)
    
# Step 1: Define a function to read and preprocess text data from multiple files.
def read_and_preprocess_data(file_paths):
    data = []
    labels = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # Perform any necessary data preprocessing here, such as text cleaning.
            # You can use regular expressions or other techniques to clean the text.
            data.append(content)
            labels.append(os.path.basename(file_path).split('.')[0])  # Use the file name as a label.
    return data, labels

# Step 4: Read and preprocess the data.
data, labels = read_and_preprocess_data(file_paths)

text_rec = 'voice'
lent = (text_rec.split(' '))
for itrn in range(0,len(lent)):
        
    reviews = lent[itrn]
    default_ans = data
    
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    cosine_sim = []
    for ii in range(0,len(data)):
        
        # Two strings to compare
        string1 = default_ans[ii]
        string2 = reviews
        
        # Initialize the TF-IDF vectorizer
        vectorizer = TfidfVectorizer()
        
        # Transform the strings into TF-IDF vectors
        tfidf_matrix = vectorizer.fit_transform([string1, string2])
        
        # Calculate the cosine similarity between the vectors
        cosine_sim.append(cosine_similarity(tfidf_matrix[0], tfidf_matrix[1]))
        res = np.max(cosine_sim)
    print("Cosine Similarity:", cosine_sim)
    
    IDX.append(cosine_sim.index(res))

Laudio = []

from pydub import AudioSegment
from pydub.playback import play
import noisereduce as nr
for itrn in range(0,len(lent)):  
    
    
    # from scipy.io import wavfile
    # samplerate, data = wavfile.read('res.wav')
        
    # from scipy.io import wavfile
    # samplerate, data = wavfile.read('res.wav')
    
    # file1 = open("Text/"+str(IDX[itrn])+".txt","r")
    # Voice_ch = file1.read()


    # Load the audio file
    # samplerate1, data1 = wavfile.read("Me/"+str(IDX)+".wav")

    Laudio = AudioSegment.from_file("Me/"+str(arr[IDX[itrn]])+".wav", format="wav")
    # filtered_audio = audio.low_pass_filter(0.01)
    
    
    # Change the pitch
    octaves = 0.9  # You can adjust this value to change the pitch
    new_audio = Laudio.speedup(playback_speed=1.3 / octaves)
    
    
    # Play the modified audio
    play(new_audio)
    
    
    # Save the modified audio to a new file
    new_audio.export("Final_res.wav", format="wav")
