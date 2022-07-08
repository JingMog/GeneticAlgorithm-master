from PIL import Image
import random

# path = 'D:\.automation\python\GeneticAlgorithm\chrome.png'
savepath = './'
ori_img= 'D:/chrome.png'


# 随机蒙塔卡罗
def initialpop(width, height):
    population = []
    for i in range(height):
        temp = []
        for j in range(width):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            temp.append([r,g,b])
        population.append(temp)
    return population


# 读取图像
def ReadImg(path):
    img = Image.open(path)
    elem = []
    width, height = img.size
    for j in range(height):
        temp = []
        for i in range(width):
            r, g, b = img.getpixel((i, j))[:3]  # 获取像素块的r,g,b值
            temp.append([r, g, b])
        elem.append(temp)  # elem为3维,elem[i][j]代表第i,j个像素块的r,g,b列表
    return elem, img.size

# 随机产生r,g,b值
# 参数分别为当前种群和目标种群属性
def Evolution(population, target, width, height):
    for i in range(width):
        for j in range(height):
            # 如果种群不一样则随机产生新的值
            if(population[i][j][0] != target[i][j][0]):
                population[i][j][0] = random.randint(0,255)
            if(population[i][j][1] != target[i][j][1]):
                population[i][j][1] = random.randint(0,255)
            if(population[i][j][2] != target[i][j][2]):
                population[i][j][2] = random.randint(0,255)
    return population  # 返回生成的新种群

# 根据种群保存生成的图像
def SaveImg(population, ori_img, generation):
    img = Image.open(ori_img)
    for j, row in enumerate(population):
        for i, col in enumerate(row):
            r, g, b = col
            img.putpixel((i,j), (r, g, b))
    img.save("{}.png".format(generation))

def run():
    generation = 0  # 迭代次数
    target, size = ReadImg(path=ori_img)  # 读取图像
    population = initialpop(width=size[0],height=size[1])  # 初始化种群
    # print(data[0][0])
    for i in range(5000):
        generation += 1
        population = Evolution(population=population, target=target, width=size[1], height=size[0])
        print(generation)
        if generation % 100 == 0:
            SaveImg(population,ori_img,generation)
            print("save img {}.png".format(generation))


run()
# population = initialpop(30,30)
# SaveImg(population=population,ori_img='D:/chrome.png',generation=1)
# data,size = ReadImg(ori_img)