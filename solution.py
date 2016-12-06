#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import json
jsonFile = open('input.json', 'r')
values = json.load(jsonFile)
jsonFile.close()

#object to store the id of the user and the questions answered
class id:
	 def __init__(self):
	 	 	self.number = 0
			self.questions = []

#object to store the fields related to a question such as question id, users answer, importance etc.
class questionId:
    def __init__(self):
    	self.number = 0
        self.answer = 0
        self.acceptableAnswers = []
        self.importance = 0

#list to store all users 
ids = []

#temporary list to store all questions a particular user has answered 
questions = []

#parsing json object to extract data from input file and to store appropriately 
for profile in values['profiles']:
    for answer in profile['answers']:
    	tempqid = questionId()
        tempqid.number = answer['questionId']
        tempqid.answer = answer['answer']
        tempqid.importance = answer['importance']
        for acceptableAnswer in answer['acceptableAnswers']:
        	tempqid.acceptableAnswers.append(acceptableAnswer)
        questions.append(tempqid)
    tempid = id()
    tempid.number = profile['id']
    tempid.questions = questions
    ids.append(tempid)
    questions = []

#object to store all matches and scores for each match for a particular user id 
class matches:
	def __init__(self):
	 	 	self.id = 0
	 	 	self.scoreids = {0:0}
	 	 	self.scores = []

IMPORTANCE_POINTS = [0, 1, 10, 50, 250]
compareids = ids
arrayOfMatches = []
tempmatches=[]

#traversing all users
for i in ids:
	dictForScores = {0:0}
	tempscoresforsort = []
	#nested for loop to compare users to determine match
	for j in compareids:
		#if user id's differ -- making sure i dont compare the same user with him/herself
		if i.number != j.number:
			countCommonQuestions = 0
			totalimportancesA = 0
			totalmatchedvalueA = 0
			totalimportancesB = 0
			totalmatchedvalueB = 0
			for qs in i.questions:
				for chqs in j.questions:
					#checking to see if the two users have answered identical questions so to calculate score
					if qs.number == chqs.number:
						if chqs.answer in qs.acceptableAnswers:
							totalmatchedvalueA = totalmatchedvalueA + IMPORTANCE_POINTS[qs.importance]
						totalimportancesA = totalimportancesA + IMPORTANCE_POINTS[qs.importance]
						if qs.answer in chqs.acceptableAnswers:
							totalmatchedvalueB = totalmatchedvalueB + IMPORTANCE_POINTS[chqs.importance]
						totalimportancesB = totalimportancesB + IMPORTANCE_POINTS[chqs.importance]
						countCommonQuestions = countCommonQuestions + 1
			if countCommonQuestions == 0:
				score = 0
			else:
 				score = math.sqrt(((totalmatchedvalueA*100)/totalimportancesA)*((totalmatchedvalueB*100)/totalimportancesB)) - (1/countCommonQuestions)
 			tempscoresforsort.append(score)
 			dictForScores.update({score:j.number})
 	tmpch = matches()
	tmpch.id = i.number
	tmpch.scoreids = dictForScores
	tmpch.scores = tempscoresforsort
	tempmatches.append(tmpch)

for match in tempmatches:
	i = 0
	print "profiled " + str(match.id) 
	print "matches:"
	while i < 10 and i < len(match.scores):
		match.scores.sort(reverse=True)
		print '\t' + "profiled = " + str(match.scoreids[match.scores[i]]) + ", score = " + str(match.scores[i])
		i = i + 1
	


