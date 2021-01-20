# <center> Gomoku</center>

- [x] Implement Minimax with Alpha-Beta Pruning in your agent.

  ```txt
  code
  └─ MCTS
         ├─ AI-Template.py
         ├─ mcts.py
         ├─ pisqpipe.py
         └─ utils.py
  └─ pbrain-abpruning
         ├─ AI-template.py
         ├─ board.py
         ├─ abpruning.py
         ├─ pisqpipe.py
         └─ utils.py
  ```

  - Command to compile the code to an executable file after unzip:

  ```txt
  cd pbrain-abpruning
  pyinstaller utils.py abpruning.py AI-template.py pisqpipe.py --name pbrain-abpruning.exe --onefile
  cd MCTS
  pyinstaller utils.py abpruning.py AI-Template.py pisqpipe.py --name pbrain-mcts.exe 
  --onefile
  ```

  

- [x] Implement MCTS and improve your agents.

