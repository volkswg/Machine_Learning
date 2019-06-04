import numpy as np
import operator

class World:
	## Initialise starting data
	def __init__(self):
		# Set information about the gridworld
		self.height = 10
		self.width = 10
		self.grid = np.zeros(( self.height, self.width)) - 1
		
		# Set random start location for the agent
		self.current_location = (np.random.randint(1,3), np.random.randint(1,3))
		
		# Set locations for the bomb and the gold
		self.bomb_location1 = (np.random.randint(3,7),np.random.randint(5,8))
		self.bomb_location2 = (np.random.randint(3,7),np.random.randint(5,8))
		while self.bomb_location1 == self.bomb_location2:
			self.bomb_location2 = (np.random.randint(3,7),np.random.randint(5,8))
		self.gold_location = (9,9)
		self.terminal_states = [ self.bomb_location1,  self.bomb_location2, self.gold_location]
		
		# Set grid rewards for special cells
		self.grid[ self.bomb_location1[0], self.bomb_location1[1]] = -10
		self.grid[ self.bomb_location2[0], self.bomb_location2[1]] = -10
		self.grid[ self.gold_location[0], self.gold_location[1]] = 20
		self.grid[0:2,[4,5,6,7,8]] = -20 #Cliff
		self.grid[[5,6,7,8,9],4] = -20 #Cliff
		self.grid[8,8] = -20 #Cliff
		
		# Set available actions
		self.actions = ['up', 'down', 'left', 'right']

	def reset(self):
		# Set random start location for the agent
		self.current_location = (np.random.randint(1,3), np.random.randint(1,3))
		# Set locations for the bomb and the gold
		self.bomb_location1 = (np.random.randint(6,9),np.random.randint(6,9))
		self.bomb_location2 = (np.random.randint(5,8),np.random.randint(5,8))
		while self.bomb_location1 == self.bomb_location2:
			self.bomb_location2 = (np.random.randint(5,8),np.random.randint(5,8))
	
		
	## Put methods here:
	def available_actions(self):
		"""Returns possible actions"""
		return self.actions
	
	def render(self):
		"""Prints out current location of the agent on the grid (used for debugging)"""
		grid = np.zeros(( self.height, self.width))
		grid[ self.current_location[0], self.current_location[1]] = 1
		grid[ self.bomb_location1[0], self.bomb_location1[1]] = -10
		grid[ self.bomb_location2[0], self.bomb_location2[1]] = -10
		grid[ self.gold_location[0], self.gold_location[1]] = 10
		grid[0:2,[4,5,6,7,8]] = -20 #Cliff
		grid[[5,6,7,8,9],4] = -20
		grid[8,8] = -20 #Cliff
		return grid
	
	def get_reward(self, new_location):
		"""Returns the reward for an input position"""
		return self.grid[ new_location[0], new_location[1]]
		
	
	def move_agent(self, action):
		"""Moves the agent in the specified direction. If agent is at a border, agent stays still
		but takes negative reward. Function returns the reward for the move."""
		# Store previous location
		last_location = self.current_location
		
		# UP
		if action == 'up':
			# If agent is at the top, stay still, collect reward
			if last_location[0] == 0:
				reward = self.get_reward(last_location)
			else:
				self.current_location = ( self.current_location[0] - 1, self.current_location[1])
				reward = self.get_reward(self.current_location)
		
		# DOWN
		elif action == 'down':
			# If agent is at bottom, stay still, collect reward
			if last_location[0] == self.height - 1:
				reward = self.get_reward(last_location)
			else:
				self.current_location = ( self.current_location[0] + 1, self.current_location[1])
				reward = self.get_reward(self.current_location)
			
		# LEFT
		elif action == 'left':
			# If agent is at the left, stay still, collect reward
			if last_location[1] == 0:
				reward = self.get_reward(last_location)
			else:
				self.current_location = ( self.current_location[0], self.current_location[1] - 1)
				reward = self.get_reward(self.current_location)

		# RIGHT
		elif action == 'right':
			# If agent is at the right, stay still, collect reward
			if last_location[1] == self.width - 1:
				reward = self.get_reward(last_location)
			else:
				self.current_location = ( self.current_location[0], self.current_location[1] + 1)
				reward = self.get_reward(self.current_location)
				
		return reward
	
	def end_state(self):
		"""Check if the agent is in a terminal state (gold or bomb), if so return 'DONE'"""
		if self.current_location in self.terminal_states:
			return True
		else:
			return False