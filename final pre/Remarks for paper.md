# Remarks

- **A Contextual-Bandit Approach to Personalized News Article Recommendation** [[paper](https://arxiv.org/abs/1003.0146)] *Lihong Li, Wei Chu, John Langford, Robert E. Schapire* 2010.02 WWW '10: Proceedings of the 19th international conference on World wide web

https://banditalgs.com/2016/10/19/stochastic-linear-bandits/

https://courses.cs.washington.edu/courses/cse599i/18wi/resources/lecture10/lecture10.pdf

### Contextual multi-armed bandits

The difference of context-free and contextual bandits is: Learner receives a context at the beginning of the round, before it needs to select its action.

### Design the model of LinearUCB

- LinUCB with disjoint linear models

For LinUCB, we assume reward for arm $a$ at time step $t$ is based on a linear model:
$$
r_{a,t}=\mathbf x_{a,t}^T\theta_a^*+\epsilon_t
$$
where $\mathbf x \in \mathbb R^d$ is a d-dimentional feature with inner product to unknown coefficients$\theta^*_a$ for each arm, and we assume $\epsilon$ to be 1-subgaussian

In order to calculate the cumulative reward, LinUCB define some variables:

$\mathbf X_{a,t}=[\mathbf x_{a,1} ...\mathbf x_{a,t}]^T$: t contexts previously observed for arm a

$\Gamma_{a,t} = [r_{a,1}...r_{a,t}]^T$: observed reward vector

$\mathbf b_{a,t}=X_{a,t}^T\Gamma_{a,t}$: cumulative reward of arm $a$ based on context

If we successfully learn the parameter, pick the largest reward arm and pull, then update the context, then how to learn the linear model parameter? **Ridge Regression**: the result result is: $\hat \theta_{a,t}=(\mathbf X_{a,t}^T\mathbf X_{a,t} + \lambda\mathbf I)^{-1}\mathbf X_{a,t}^T\Gamma_{a,t}$, and to be simple, we denote $\mathbf A_{a,t}=\mathbf X_{a,t}^T\mathbf X_{a,t} + \lambda\mathbf I$, then $\hat\theta_{a,t} = \mathbf A_{a,t}^{-1}\mathbf b_{a,t}$

Designing algorithm with one hyperparam $\alpha$ to control the upper confidence bound （Paper: LinUCB with disjoint linear models)

- LinUCB with hybrid linear models

Add one term that corresponed to a shared parameter for all arms
$$
r_{a,t}=\mathbf x_{a,t}^T\theta_a^*+\mathbf z_{a,t}^T\beta^*+\epsilon_t
$$
where $\mathbf z_{a,t} \in \mathbb R^k$ is a shared feature for all arms, and $\beta^*$ is the shared parameter for each arm

### Experiments

- Data collection, preprocessing and dimension reduction

Event info: chosen article, user/article info, whether clicked on story position(most obvious position)

Training set: 4.7 million data on May 01

Testing set: 36 million events from May 03-09



Feature extracted(10 means separated into 10 groups): 

user info(gender(2), age(10), location in U.S.(200), consumption history(2*1000))

article info(URL categories(10), tag(10), encoded feature(?))



Dimension reduction for users: Logistic regression to appoximate user/article feature, K-means to cluster raw users feature, use gaussian kernel to normalize 5 clusters into 5 dims, and add one more dim and set 1

Result: each article $a$ has a distinctive 6-dim feature for user $u$(separate feature for each arm), and 6-dim article feature(shared feature for all arms), which has a outer product for 36 dims.

- Compared algorihms

Reward: CTR (click-through rate)
$$
CTR=\frac{\text{number of clicks}}{\text{number of impressions}} \times 100\%
$$


1. Random(pick arbitrary article for the user, baseline)
2. $\epsilon$-greedy
3. UCB1
4. LinUCB
5. Omniscient: precalculate the click rate for article and users, then choose the best one

(Lot's of details in the paper...)

- Results:

1. When the parameter (ǫ or α) is too small, there was insufficient exploration. On the other hand, when the parameter is too large, the algorithms appeared to over-explore and thus wasted some of the opportunities to increase the number of clicks. Based on these plots on tuning data, we chose **appropriate parameters** for each algorithm and ran it once on the evaluation data in the next subsection.

2. Discussion about warm start(pretrain the logistic regression model with data from Sept 2008): $\epsilon$-greedy gain more stable performance, but warm up did not help ucb
3. All algorithms performs better than context free $\epsilon$-greedy, and ucb with linucb outperforms $\epsilon$-greedy algorithm
4. No distinguishment for UCB and LinUCB could be found in the experiment since many features are dominant..

