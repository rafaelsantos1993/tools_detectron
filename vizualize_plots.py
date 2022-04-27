#Class to vizualize plots from the output json file 
#made by detectron2

import json 
import matplotlib.pyplot as plt 
import json 
import pandas as pd 

#class get the plots of losses, APs, and AP maxs

class get_plots(object):
    def __init__ (self, json_path):
        self.json_path = json_path

        #gets the annotations and makes a dataframe out of it

        lines=[]

        with open(json_path, 'r') as f:
            for line in f:
                lines.append(json.loads(line))
    
        self.df_results=pd.DataFrame(lines)

    #gets the training and validation results in terms of the total losses 
    
    def get_loss_train_validation(self):

        #filtering loss results that are not null for both traning and validation 

        df_results = self.df_results

        validation_not_null = df_results[df_results.validation_loss.notnull()]
        validation_loss_not_null=validation_not_null[validation_not_null.total_loss.notnull()]

        #get the values of traning, validation and iteration 
        training_loss=validation_loss_not_null.total_loss
        validation_loss=validation_loss_not_null.validation_loss
        iteration = validation_loss_not_null.iteration

        #plot 
        plt.figure(figsize = (16,8))
        plt.plot(iteration,training_loss, label = 'training losses')
        plt.plot(iteration,validation_loss, label = 'validation losses')
        plt.legend(loc = 'upper right')
        plt.xlabel('Iteration')
        plt.ylabel('Total Loss')
        plt.show()

    def get_aps_plots (self):
        
        #gets the values of AP50 and AP 50 for bbox and segmentation 

        df_results=self.df_results

        sAP50 = df_results[df_results['segm/AP50'].notnull()]
        iteration = sAP50['iteration'].values
        sAP50 = sAP50['segm/AP50'].values 
        bAP50 = df_results[df_results['segm/AP50'].notnull()]
        bAP50 = bAP50['bbox/AP50'].values
        sAP75 = df_results[df_results['segm/AP75'].notnull()]
        sAP75 = sAP75['segm/AP75'].values
        bAP75 = df_results[df_results['segm/AP75'].notnull()]
        bAP75 = bAP75['bbox/AP75'].values
        
        #ploting 
        plt.figure(figsize = (16,8))
        plt.plot(iteration,sAP50, marker ='o', label = 'Segm/AP50')
        plt.plot(iteration,bAP50,marker ='o', label = 'Bbox/A50')
        plt.plot(iteration,sAP75, marker ='x', label = 'Segm/AP75')
        plt.plot(iteration,bAP75,marker ='x', label = 'Bbox/AP75')
        plt.legend(loc = 'upper left')
        plt.xlabel('Iteration')
        plt.ylabel('Total Loss')
        plt.show()
    
    def get_apm_plots(self):

        #plots apms vs iterations 

        df_results=self.df_results

        bbox_apms = df_results[df_results['bbox/APm'].notnull()]['bbox/APm']
        seg_apms = df_results[df_results['segm/APm'].notnull()]['segm/APm']
        iteration = df_results[df_results['bbox/APm'].notnull()]['iteration']


        plt.figure(figsize = (16,8))
        plt.plot(iteration,bbox_apms, label = 'apm_bbox')
        plt.plot(iteration,seg_apms, label = 'apm_segm')
        plt.legend(loc = 'upper right')
        plt.xlabel('Iteration')
        plt.ylabel('APm')
        plt.show()

    def get_maximuns(self):

        #gets the maximum of APm, bbox and segm AP50 and AP75

        df_results=self.df_results
        
        maximuns = pd.DataFrame (columns = ['Max','Iteration'], index = ['APm/bbox','APm/segm','bbox/AP50','bbox/AP75','segm/AP50','segm/AP75']) # creates the dataframe
        maximuns.loc[['APm/bbox'],['Iteration']] = df_results[df_results['bbox/APm'] == df_results['bbox/APm'].max()]['iteration'].values[0] #filters to get the iteration number where the APm bbox is maximum 
        maximuns.loc[['APm/bbox'],['Max']] = df_results['bbox/APm'].max() #get the actual maximum value 

        #maximum for segmentation
        maximuns.loc[['APm/segm'],['Iteration']] = df_results[df_results['segm/APm'] == df_results['segm/APm'].max()]['iteration'].values[0] 
        maximuns.loc[['APm/segm'],['Max']] = df_results['segm/APm'].max() 

        # Repeat the same AP50 and AP75 

        maximuns.loc[['bbox/AP50'],['Iteration']] = df_results[df_results['bbox/AP50'] == df_results['bbox/AP50'].max()]['iteration'].values[0] 
        maximuns.loc[['bbox/AP50'],['Max']] = df_results['bbox/AP50'].max() 

        maximuns.loc[['segm/AP50'],['Iteration']] = df_results[df_results['segm/AP50'] == df_results['segm/AP50'].max()]['iteration'].values[0] 
        maximuns.loc[['segm/AP50'],['Max']] = df_results['segm/AP50'].max() 

        maximuns.loc[['bbox/AP75'],['Iteration']] = df_results[df_results['bbox/AP75'] == df_results['bbox/AP75'].max()]['iteration'].values[0] 
        maximuns.loc[['bbox/AP75'],['Max']] = df_results['bbox/AP75'].max() 

        maximuns.loc[['segm/AP75'],['Iteration']] = df_results[df_results['segm/AP75'] == df_results['segm/AP75'].max()]['iteration'].values[0] 
        maximuns.loc[['segm/AP75'],['Max']] = df_results['segm/AP75'].max() 

        return maximuns