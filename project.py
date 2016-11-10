#! /usr/bin/python
import sys
import numpy as np
import matplotlib.pyplot as plot

def printgrid(grid):
	'''function to print the grid passed into it'''
	for row in grid:
		newRow = ""
		for each in row:
			newRow += str(each)
			newRow += "\t"
		print(newRow)

def displaygrids(animal, food):
	'''function to nicely display the animal grid and food grid passed to it'''
	print("---------------------------------------")
	print("Animal Grid:")
	printgrid(animal)
	print("Food Grid:")
	printgrid(food)
	print("---------------------------------------")

def displayplots(animal, food):
	plot.subplot(212)
	plot.imshow(food, interpolation = "nearest", cmap = "Blues")
	plot.colorbar()
	plot.title('Food')
	plot.subplot(211)
	plot.imshow(animal, interpolation = "nearest", cmap = "Reds")
	plot.colorbar()
	plot.title('Animals')
	#output to files for each generation, labelled with currentgeneration_eatingrate_growthrate_maxfood_foodforbreeding
	plot.savefig("gen"+str(generation-1)+"_"+str(eatrate)+"_"+str(growrate)+"_"+str(maxfood)+"_"+str(breedthreshold)+".png")
	plot.show()

#gridRow = input("How many rows: ")
#gridColumn = input("How many columns: ")

gridRow = 6
gridColumn = 6

eatrate = 10
growrate = 10
maxfood = 100
breedthreshold = 20
generation = 0

animalgrid = np.zeros((gridRow,gridColumn), np.int8)
foodgrid = np.full((gridRow,gridColumn), maxfood, np.int8)

startinganimals = input("How many animals to start: ")
for each in range(startinganimals):
	inputRow = input("Starting animal row: ")
	inputColumn = input("Starting animal column: ")
	inputRow -= 1
	inputColumn -= 1
	animalgrid[inputRow, inputColumn] = 1
	print("")

displaygrids(animalgrid, foodgrid)
#displayplots(animalgrid, foodgrid)

generation = 1
finalgeneration = 20

while generation <= finalgeneration:
	#food regrows as per the growth rate ready for next generation, to a max level
	for eachrow in range(gridRow):
		for eachcolumn in range(gridColumn):
			foodgrid[eachrow, eachcolumn] += growrate
			if foodgrid[eachrow, eachcolumn] > maxfood:
				foodgrid[eachrow, eachcolumn] = maxfood
			elif foodgrid[eachrow, eachcolumn] <= 0:
				foodgrid[eachrow, eachcolumn] = 100
	animalcount = 0
	#create or reset newgrid, a temporary grid that stores surviving and bred animals for the turn
	newgrid = np.zeros((gridRow,gridColumn), np.int8)
	for rows in range(gridRow):
		for cols in range(gridColumn):
			#create or reset breedgrid, a temporary grid that stores the current animal's survival, death or breeding pattern, to eventually be passed to newgrid
			breedgrid = np.zeros((gridRow,gridColumn), np.int8)
			if animalgrid[rows,cols] == 1:
				#for adjacent cells, MAX excludes negative values, MIN excludes values over grid parameters
				eaten = 0
				for foodrow in range(max(0, rows-1), min(gridRow, rows+2)):
					for foodcol in range(max(0, cols-1), min(gridColumn, cols+2)):
						if foodgrid[foodrow, foodcol] > eatrate:
							eaten += eatrate
							foodgrid[foodrow, foodcol] -= eatrate
						elif foodgrid[foodrow, foodcol] <= eatrate:
							eaten += foodgrid[foodrow, foodcol]
							foodgrid[foodrow, foodcol] = 0
				if eaten >= breedthreshold:
					#populate cells straight next to sufficiently fed animal
					#if statements to stop it being out of range, but quite a dirty way, can it be cleared up?
					if rows-1 >= 0 and rows-1 < gridRow and cols >= 0 and cols < gridColumn:
						breedgrid[rows-1,cols] = 1
					if rows >= 0 and rows < gridRow and cols-1 >= 0 and cols-1 < gridColumn:					
						breedgrid[rows, cols-1] = 1
					if rows >= 0 and rows < gridRow and cols >= 0 and cols < gridColumn:
						breedgrid[rows, cols] = 1
					if rows >= 0 and rows < gridRow and cols+1 >= 0 and cols+1 < gridColumn:
						breedgrid[rows, cols+1] = 1
					if rows+1 >= 0 and rows+1 < gridRow and cols >= 0 and cols < gridColumn:
						breedgrid[rows+1, cols] = 1
				elif eaten == 0:
					#do not populate the cell of the animal, it dies from no food
					print("Animal died")
				else:
					#repopulate cell of animal without breeding
					breedgrid[rows, cols] = 1
			#transfer animals from breedgrid over to newgrid (adding to newgrid, not just copying)
			for breedrows in range(gridRow):
				for breedcols in range (gridColumn):
					if breedgrid[breedrows, breedcols] == 1:
						newgrid[breedrows, breedcols] = 1
	animalgrid = newgrid
	#kill animals with no food surrounding them
	for Row in range(gridRow):
		for Col in range(gridColumn):
			if foodgrid[Row,Col] <= 0:
				animalgrid[Row,Col] = 0
	print ("-----")
	#displays the generation 
	print "Generation", generation, ":"
	displaygrids(animalgrid, foodgrid)
	generation += 1

	#displays animal and food grids as heatmap images for each generation
	displayplots(animalgrid, foodgrid)
