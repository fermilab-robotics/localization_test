import matplotlib.pyplot as plt
import numpy as np

def parse_location_csv(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        header = lines[0].split(',')
        
        bot_odom_x = []
        bot_odom_y = []
        bot_odom_z = []

        bot_vis_x  = []
        bot_vis_y  = []
        bot_vis_z  = []
        
        for line in lines[1:]:
            bot_odom_x.append(float(line.split(',')[header.index('bot_odom_x')]))
            bot_odom_y.append(float(line.split(',')[header.index('bot_odom_y')]))
            bot_odom_z.append(float(line.split(',')[header.index('bot_odom_z')]))
            bot_vis_x.append(float(line.split(',')[header.index('bot_vis_x')]))
            bot_vis_y.append(float(line.split(',')[header.index('bot_vis_y')]))
            bot_vis_z.append(float(line.split(',')[header.index('bot_vis_z')]))
    
    bot_odom = [np.asarray(bot_odom_x), np.asarray(bot_odom_y), np.asarray(bot_odom_z)]
    bot_vis  = [np.asarray(bot_vis_x), np.asarray(bot_vis_y), np.asarray(bot_vis_z)]

    return bot_odom, bot_vis

directory = './Data/Mar18Test/'
filename = 'localization_test_output_20220318-141929.csv'
bot_odom, bot_vis = parse_location_csv(directory+filename)

plt.figure(figsize=(10,8))
plt.suptitle('Visual summary of %s'%(filename))
plt.subplot(211)
plt.plot(bot_odom[0], 'o', label="odom_x")
plt.plot(bot_odom[1], 'o', label="odom_y")
plt.plot(bot_odom[2], 'o', label="odom_z")
plt.legend()
plt.gca().set_facecolor("#F1F1F1")
plt.grid()

plt.subplot(212)
plt.plot(bot_vis[0], 'o', label="vis_x")
plt.plot(bot_vis[1], 'o', label="vix_y")
plt.plot(bot_vis[2], 'o', label="vix_z")
plt.legend()
plt.gca().set_facecolor("#F1F1F1")
plt.grid()
#plt.show()
plt.savefig('%s.png'%(filename.strip('.csv')))
