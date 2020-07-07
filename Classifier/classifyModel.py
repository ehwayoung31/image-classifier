from fastai.vision import *
defaults.device = torch.device('cpu')
img = image_file

path=Path('classifier/data')
learn = load_learner(path)

pred_class,pred_idx,outputs = learn.predict(img)
pred_class
