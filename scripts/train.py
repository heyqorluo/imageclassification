from matplotlib import pyplot as plt
from tensorflow.keras import datasets, layers, models
import os
import random
import tensorflow as tf 

MODEL_NAME ="model"
CLASS_NAME = ['airplane','automobile','bird','cat','deer','dog','frog','horse','ship','truck']

def plot_sample_images(images,labels):
    plt.figure(figsize=(10,10))
    for i in range (25):
        n = random.randint(0,len(images))
        plt.subplot(5,5,i+1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(images[n])
        plt.xlabel(CLASS_NAME[labels[n][0]])
    plt.savefig(os.path.join('output',"sample_image.jpg"))    

def create_model():
    model = models.Sequential()
    #Add convolutinal layers
    model.add(layers.Conv2D(32,(3,3), activation = "relu",input_shape= (32,32,3)))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D(2,2))
    model.add(layers.Dropout(0.25))
    
    model.add(layers.Conv2D(64,(3,3), activation = "relu"))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D(2,2))
    model.add(layers.Dropout(0.25))
    
    model.add(layers.Conv2D(128,(3,3), activation = "relu"))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D(2,2))
    model.add(layers.Dropout(0.25))
    
    model.add(layers.Flatten())
    
    # Add dense layers
    model.add(layers.Dense(128,activation = "relu"))
    model.add(layers.BatchNormalization())
    model.add(layers.Dropout(0.5))
    
    model.add(layers.Dense(10, activation = "softmax"))
   
    return model 

def plot_training_history(history):
    plt.figure(figsize = (10,10))
    plt.plot(history.history["accuracy"],label = "accuracy")
    plt.plot(history.history["val_accuracy"],label = "val_accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.ylim([0.0,1.0])
    plt.legend(loc = "lower right")
    plt.savefig(os.path.join("output","training_history.png"))


if __name__ =="__main__":
    if not os.path.isdir("output"):
        os.mkdir("output")


    # load data
    (train_image,train_labels),(test_image,test_labels)= datasets.cifar10.load_data()
    plot_sample_images(train_image, train_labels)
    # nomalise the data
    train_image,test_image = train_image/255.0,test_image/255.0
    #create model
    model = create_model()
    model.summary()
    
    # train the model
    model.compile(optimizer = "adam",loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),metrics=["accuracy"])
    
    history = model.fit(train_image,train_labels,epochs = 20, validation_data=(test_image,test_labels))
    plot_training_history(history)
    
    # Evaluate the model
    test_loss,test_acc = model.evaluate(test_image, test_labels,verbose = 2)
    print (f"Test accuracy:{test_acc}%")
    
    # Save the model
    model.save(os.path.join("output",f"{MODEL_NAME}.h5"))
    
