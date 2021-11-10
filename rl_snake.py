from tensorflow.python.keras.layers.pooling import Pooling2D
from snake import SnakeEnv
from tensorflow.keras.models import Sequential
from tensorflow.keras import Model, Input
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Permute
from tensorflow.keras.optimizers import Adam
from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

env = SnakeEnv()

## -------------- Random choices -----------------
# episodes = 1000
# for episode in range(1,episodes):
# 	state = env.reset()
# 	done = False
# 	score = 0
# 	timesteps = 0

# 	while not done:
# 		timesteps += 1
# 		action = env.action_space.sample()
# 		n_state, reward, done, info = env.step(action)
# 		score += reward
	
# 	print(f'Episode: {episode} | timesteps: {timesteps} | score: {score}')
## ------------------------------------------------

# --------------- Learned choices ----------------
WINDOW_LENGTH = 5
inputs = Input(shape=(WINDOW_LENGTH,) + env.state.shape)	# NOTE: input is WINDOW_LENGTH lots of the state grid.
x = Permute((2,3,1))(inputs)	# Re-order axis to be (row,cols,channels)
x = Conv2D(5,(5,5),strides=(2,2))(x)	# Conv2D does not implement data_format='channels_first' on CPU.
x = MaxPooling2D(pool_size=(2,2),strides=(2,2))(x)
x = Flatten()(x)
x = Dense(50,activation='relu')(x)
x = Dense(50,activation='relu')(x)
output = Dense(env.action_space.n,activation='linear')(x)
model = Model(inputs=inputs,outputs=output)
print(model.summary())


policy = BoltzmannQPolicy()
memory = SequentialMemory(
	limit=50000,	# Maximum size of memory. As new experiences are added to this memory and it becomes full, old experiences are forgotten.
	window_length=WINDOW_LENGTH
)
# Some notes below from: https://hub.packtpub.com/build-reinforcement-learning-agent-in-keras-tutorial/
dqn = DQNAgent(
	model=model,	# A keras model
	memory=memory,	# The rl.memory object to save the experiences to.
	policy=policy,	# A keras-rl policy
	nb_actions=env.action_space.n,	# Number of available actions for agent to use..?
	nb_steps_warmup=10,	# Determines how long we wait before we start doing experience replay. This lets us build up enough experience to build a proper minibatch.
	target_model_update=1e-2	# The Q function is recursive and when the agent updates it’s network for Q(s,a) that update also impacts the prediction it will make for Q(s’, a). This can make for a very unstable network. The way most deep Q network implementations address this limitation is by using a target network, which is a copy of the deep Q network that isn’t trained, but rather replaced with a fresh copy every so often. The target_model_update parameter controls how often this happens.
)	# target_model_update >= 1, the target model is updated every target_model_update-th step. target_model_update < 1, we use something called soft updates. The idea here is similar but instead of updating the entire target model (hard update), we gradually adopt changes like so: target_model = target_model_update * target_model + (1 - target_model_update) * model (https://github.com/keras-rl/keras-rl/issues/55)

dqn.compile(Adam(lr=0.001),metrics=['mse'])
dqn.fit(env,nb_steps=50000,visualize=True,verbose=1)

# -------------------------------------------------
