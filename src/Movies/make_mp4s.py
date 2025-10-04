import numpy as np
import cv2

for ix in range(3):
    movie = np.load(f'Movie_TOE{ix+1}.npy')
    shuffled_frames = np.random.permutation(movie.shape[0])

    writer = cv2.VideoWriter(f'natural_movie_TOE_{ix+1}.mp4',
                             cv2.CAP_MSMF,
                             cv2.VideoWriter_fourcc(*'avc1'),
                             30,
                             (movie.shape[2],movie.shape[1]),
                             isColor=True)
    
    writer_shuffle = cv2.VideoWriter(f'natural_movie_TOE_{ix+1}_shuffle.mp4',
                                     cv2.CAP_MSMF,
                                     cv2.VideoWriter_fourcc(*'avc1'),
                                     30,
                                     (movie.shape[2],movie.shape[1]),
                                     isColor=True)
    
    try:
        for f in range(movie.shape[0]):
            writer.write(cv2.cvtColor(movie[f],cv2.COLOR_GRAY2BGR))
            writer_shuffle.write(cv2.cvtColor(movie[shuffled_frames[f]],cv2.COLOR_GRAY2BGR))
    finally:
        writer.release()
        writer_shuffle.release()