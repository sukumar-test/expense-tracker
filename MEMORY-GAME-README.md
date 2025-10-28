# Memory Card Game

A fun and interactive memory card matching game built with Node.js.

## Features

- **Classic Memory Game**: Match pairs of emoji cards
- **Move Counter**: Tracks the number of moves you make
- **Timer**: Tracks how long it takes to complete the game
- **Statistics**: Keeps track of your best score
- **Responsive Design**: Works on desktop and mobile devices
- **Beautiful UI**: Modern gradient design with smooth animations

## How to Play

1. Click on cards to flip them over
2. Try to find matching pairs
3. Match all pairs to win
4. Try to complete the game in the fewest moves possible

## Getting Started

### Prerequisites

- Node.js (v12 or higher)

### Installation

1. Navigate to the project directory:
   ```bash
   cd /home/runner/work/expense-tracker/expense-tracker
   ```

2. Install dependencies (if any):
   ```bash
   npm install
   ```

### Running the Game

Start the server:
```bash
npm start
```

Or run directly:
```bash
node memory-game.js
```

The game will be available at: http://localhost:3000

## API Endpoints

The game includes a simple REST API:

### GET /api/stats
Returns current game statistics:
```json
{
  "gamesPlayed": 0,
  "totalMoves": 0,
  "bestScore": null
}
```

### POST /api/game-complete
Submit a completed game (requires JSON body with `moves` field):
```json
{
  "moves": 12
}
```

Returns updated statistics:
```json
{
  "success": true,
  "stats": {
    "gamesPlayed": 1,
    "totalMoves": 12,
    "bestScore": 12
  }
}
```

## Project Structure

```
memory-game/
├── memory-game.js              # Node.js server
├── package.json                # NPM configuration
├── templates/
│   └── memory-game.html        # Game HTML template
└── static/
    ├── css/
    │   └── memory-game.css     # Game styles
    └── js/
        └── memory-game.js      # Game logic (client-side)
```

## Technologies Used

- **Node.js**: Server-side JavaScript runtime
- **HTTP Module**: Built-in Node.js HTTP server
- **HTML5**: Structure and semantic markup
- **CSS3**: Styling with gradients, animations, and flexbox/grid
- **Vanilla JavaScript**: Game logic without frameworks

## Game Logic

The game uses a class-based approach with the `MemoryGame` class handling:
- Card shuffling and creation
- Move tracking
- Match detection
- Timer functionality
- Win condition checking
- API communication for statistics

## Customization

You can easily customize the game by modifying:

- **Card Symbols**: Edit the `cardSymbols` array in `static/js/memory-game.js`
- **Board Size**: Adjust the grid in `static/css/memory-game.css` (`.game-board`)
- **Colors**: Change the gradient colors throughout the CSS
- **Port**: Modify the `PORT` constant in `memory-game.js`

## Future Enhancements

- Difficulty levels (easy, medium, hard)
- Different card themes
- Multiplayer mode
- Leaderboard
- Sound effects
- Persistent storage of statistics

## License

MIT License
