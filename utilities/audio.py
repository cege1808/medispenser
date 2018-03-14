import simpleaudio as sa

wave_obj = sa.WaveObject.from_wave_file('static/sound/bike_horn.wav')
play_obj = wave_obj.play()
play_obj.wait_done()