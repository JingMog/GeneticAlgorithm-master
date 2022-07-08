from lib2to3.pgen2.pgen import generate_grammar
from turtle import back
from unittest import findTestCases
from PIL import Image
import os
import math
import random
import pickle
from copy import deepcopy
from matplotlib import pyplot as plt
from numpy import size


worst_fitness = []
best_fitness = []
avg_fitness = []


# 读取图像
def GetImage(ori_img):
	img = Image.open(ori_img)
	color = []
	width, height = img.size
	for j in range(height):
		temp = []
		for i in range(width):
			r, g, b = img.getpixel((i, j))[:3]
			temp.append([r, g, b, r+g+b])
		color.append(temp)  # color为3维,color[i][j]代表第i,j个像素块的r,g,b,sum列表
	return color, img.size



# 初始化
def RandGenes(size):
	width, height = size
	genes = []
	for i in range(100):
		gene = []
		for j in range(height):
			temp = []
			for i in range(width):
				r = random.randint(0, 255)
				g = random.randint(0, 255)
				b = random.randint(0, 255)
				temp.append([r, g, b, r+g+b])
			gene.append(temp)
		genes.append([gene, 0])
	return genes


# 计算适应度
def CalcFitness(genes, target):
	total = 0
	for k, gene in enumerate(genes):
		count = 0
		for i, row in enumerate(gene[0]):
			for j, col in enumerate(row):
				t_r, t_g, t_b, t_a = target[i][j]  # 目标像素的RGB值
				r, g, b, a = col   # 当前种群基因的RGB值
				count += (abs(t_r-r) + abs(t_g-g) + abs(t_b-b))  # 累加所有像素块与目标的差值
		genes[k][1] = count  # 保存差值,genes[k][1]用来存放适应度
		total += count  # total为差值之和
	genes.sort(key = lambda x: x[1])
	best_fitness.append(genes[0][1])
	worst_fitness.append(genes[99][1])
	avg = 0
	for i in range(100):
		avg += genes[i][1]
	avg_fitness.append(avg/100)
	# print('best = {}  worst = {}'.format(genes[0][1],genes[99][1]))  # 最优值
	return genes


# 变异
def Variation(genes, target):
	rate = 0.5
	for k, gene in enumerate(genes):
		for i, row in enumerate(gene[0]):
			for j, col in enumerate(row):
				if random.random() < rate:
					a = [-1, 1][random.randint(0, 1)] * random.randint(3, 10)
					b = [-1, 1][random.randint(0, 1)] * random.randint(3, 10)
					c = [-1, 1][random.randint(0, 1)] * random.randint(3, 10)					
					if(genes[k][0][i][j][0] != target[i][j][0]):					
						genes[k][0][i][j][0] += a
					if(genes[k][0][i][j][1] != target[i][j][1]):
						genes[k][0][i][j][1] += b
					if(genes[k][0][i][j][2] != target[i][j][2]):
						genes[k][0][i][j][2] += c
					if(genes[k][0][i][j][3] != target[i][j][3]):
						genes[k][0][i][j][3] += a + b + c
	return genes


# 交叉
def Merge(gene1, gene2, size):
	width, height = size
	y = random.randint(0, width-1)
	x = random.randint(0, height-1)
	new_gene = deepcopy(gene1[0][:x])
	new_gene = [new_gene, 0]
	new_gene[0][x:] = deepcopy(gene2[0][x:])
	new_gene[0][x][:y] = deepcopy(gene1[0][x][:y])
	return new_gene


# 自然选择
def Select(genes, size):
	seek = len(genes) * 2 // 3
	i = 0
	j = seek + 1
	# j=int(len(genes)/3)+1
	# print(i,j,seek)
	while i < seek:
		genes[j] = Merge(genes[i], genes[i+1], size)
		j += 1
		i += 2
	return genes



# 保存生成的图片
def SavePic(genes, generation, ori_img):
	pic = genes
	img = Image.open(ori_img)
	for j, row in enumerate(pic):
		for i, col in enumerate(row):
			r, g, b, _ = col
			img.putpixel((i, j), (r, g, b))
	img.save("{}.png".format(generation))


# 备份
def SaveData(data, generation):
	backup = 'D:\\.automation\\python\\GeneticAlgorithm\\backup\\' + str(generation) + '.tmp'
	# fitness = 'D:\\.automation\\python\\GeneticAlgorithm\\backup\\' + 'fitness' + str(generation) + '.tmp'
	print('[INFO]: Save data to {}...'.format(backup))
	with open(backup, 'wb') as f:
	#修改保存的文件名
		pickle.dump(data, f)
	f.close()


# 读取备份
def ReadData(backup):
	print('[INFO]: Read data from {}...'.format(backup))
	with open(backup, 'rb') as f:
		data = pickle.load(f)
		genes = data['genes']
		generation = data['generation']
		best_fitness = data['best_fitness']
		worst_fitness = data['worst_fitness']
		avg_fitness = data['avg_fitness']
	f.close()
	return genes, generation, best_fitness, worst_fitness, avg_fitness



# 运行
def run(ori_img, backup, resume):
	global best_fitness, worst_fitness, avg_fitness
	data, size = GetImage(ori_img)
	if resume:
		genes, generation, best_fitness, worst_fitness, avg_fitness = ReadData(backup)
	else:
		genes = RandGenes(size)
		generation = 0
	while True:
		generation += 1
		genes = Variation(genes, data)
		genes = CalcFitness(genes, data)
		genes = Select(genes, size)
		# print('{}  best:{}   worst: {}  avg:  {}'.format(generation,
		# 				best_fitness,worst_fitness,avg_fitness))
		# print(best_fitness)
		print('{}   best: {}    worst: {}'.format(generation, best_fitness[generation-1], worst_fitness[generation-1]))
		if generation % 99999 == 0:
			databackup = {'genes': genes, 'generation': generation, 'best_fitness':best_fitness, 'worst_fitness':worst_fitness, 'avg_fitness':avg_fitness}
			# databackup = {'genes': genes, 'generation': generation}
			SaveData(databackup, generation)
			# SavePic(genes[0][0], generation, ori_img)

def fitness_gra():
	# 备份
	backup = 'D:/.automation/python/GeneticAlgorithm/backup/2500.tmp'
	genes, generation, best_fitness, worst_fitness, avg_fitness = ReadData(backup)
	x = range(0,2500)

	# 解决中文乱码
	plt.rcParams["font.sans-serif"]=["SimHei"] #设置字体
	plt.rcParams["axes.unicode_minus"]=False #正常显示负号	


	fig = plt.figure()
	ax = fig.add_axes([0.1,0.1,0.8,0.8]) # 创建axes对象
	ax.plot(x, best_fitness)
	ax.plot(x, avg_fitness)
	ax.plot(x, worst_fitness)
	ax.set_xlim(100,500)
	ax.set_ylim(150000,250000)
	# plt.plot(x,best_fitness)
	# plt.plot(x,avg_fitness)
	# plt.plot(x,worst_fitness)
	labels = ['最优适应度','平均适应度','最差适应度']
	ax.legend(labels=labels,loc='best',prop={'size':20})
	ax.set_title('遗传算法进化过程',size=20)
	ax.set_xlabel('进化代数',size=20)
	ax.set_ylabel('适应度',size=20)
	plt.tick_params(labelsize=20) #刻度字体大小13

	plt.show()


if __name__ == '__main__':
	# 备份
	backup = 'D:/.automation/python/GeneticAlgorithm/backup/2500.tmp'
	# 原始图像

	ori_img = 'D:/chrome.png'
	run(ori_img, backup, False)
	genes, generation, best_fitness, worst_fitness, avg_fitness = ReadData(backup)
	# fitness_gra()



	# resume为True则读取备份文件，在其基础上进行自然选择，交叉变异



