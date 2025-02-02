# Connect-4-Bot

### Uses Minimax Algorithm
This project utilizes the Minimax algorithm to create a simple AI bot for Connect Four. The AI evaluates smaller sections of the game board by assigning a weighted score to different positions, which it uses to make optimal decisions. Within the Minimax framework, the AI acts as the maximizing player, attempting to maximize its score, while the human player is treated as the minimizing opponent.

To enhance decision-making, the heuristic evaluation function heavily rewards situations where the AI has three of its pieces aligned, as this increases its chances of winning. Conversely, the AI loses points if the opponent has potential winning positions, encouraging it to prioritize blocking critical threats. This balance between offensive and defensive play allows the AI to make more strategic moves.

Additionally, the algorithm incorporates alpha-beta pruning to improve efficiency by reducing the number of nodes it needs to evaluate. This ensures the bot can make strong decisions within a reasonable time frame.
