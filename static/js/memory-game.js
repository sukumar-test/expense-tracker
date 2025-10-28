// Memory Game Logic
class MemoryGame {
    constructor() {
        this.cards = [];
        this.flippedCards = [];
        this.moves = 0;
        this.matchedPairs = 0;
        this.timerInterval = null;
        this.seconds = 0;
        this.isProcessing = false;

        // Card emojis for the game
        this.cardSymbols = ['🎮', '🎯', '🎨', '🎭', '🎪', '🎸', '🎺', '🎹'];

        this.init();
    }

    init() {
        this.loadStats();
        this.setupEventListeners();
        this.createBoard();
        this.startTimer();
    }

    setupEventListeners() {
        document.getElementById('new-game-btn').addEventListener('click', () => this.resetGame());
        document.getElementById('reset-stats-btn').addEventListener('click', () => this.resetStats());
        document.getElementById('play-again-btn').addEventListener('click', () => {
            this.hideWinModal();
            this.resetGame();
        });
    }

    createBoard() {
        const gameBoard = document.getElementById('game-board');
        gameBoard.innerHTML = '';

        // Create pairs of cards
        this.cards = [...this.cardSymbols, ...this.cardSymbols];
        this.shuffleArray(this.cards);

        // Create card elements
        this.cards.forEach((symbol, index) => {
            const card = this.createCard(symbol, index);
            gameBoard.appendChild(card);
        });
    }

    createCard(symbol, index) {
        const card = document.createElement('div');
        card.classList.add('card');
        card.dataset.index = index;
        card.dataset.symbol = symbol;

        const cardBack = document.createElement('div');
        cardBack.classList.add('card-back');
        cardBack.textContent = '❓';

        const cardFront = document.createElement('div');
        cardFront.classList.add('card-front');
        cardFront.textContent = symbol;

        card.appendChild(cardBack);
        card.appendChild(cardFront);

        card.addEventListener('click', () => this.handleCardClick(card));

        return card;
    }

    handleCardClick(card) {
        // Prevent clicking on already flipped or matched cards
        if (this.isProcessing || 
            card.classList.contains('flipped') || 
            card.classList.contains('matched')) {
            return;
        }

        // Flip the card
        card.classList.add('flipped');
        this.flippedCards.push(card);

        // Check for match when two cards are flipped
        if (this.flippedCards.length === 2) {
            this.moves++;
            this.updateMoves();
            this.checkForMatch();
        }
    }

    checkForMatch() {
        this.isProcessing = true;
        const [card1, card2] = this.flippedCards;

        if (card1.dataset.symbol === card2.dataset.symbol) {
            // Match found
            setTimeout(() => {
                card1.classList.add('matched');
                card2.classList.add('matched');
                this.matchedPairs++;
                this.flippedCards = [];
                this.isProcessing = false;

                // Check if game is won
                if (this.matchedPairs === this.cardSymbols.length) {
                    this.gameWon();
                }
            }, 500);
        } else {
            // No match - flip cards back
            setTimeout(() => {
                card1.classList.remove('flipped');
                card2.classList.remove('flipped');
                this.flippedCards = [];
                this.isProcessing = false;
            }, 1000);
        }
    }

    gameWon() {
        this.stopTimer();
        
        // Update final stats in modal
        document.getElementById('final-moves').textContent = this.moves;
        document.getElementById('final-time').textContent = this.formatTime(this.seconds);
        
        // Send game completion to server
        this.saveGameCompletion();
        
        // Show win modal
        setTimeout(() => {
            this.showWinModal();
        }, 500);
    }

    async saveGameCompletion() {
        try {
            const response = await fetch('/api/game-complete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    moves: this.moves,
                    time: this.seconds
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                this.updateBestScore(data.stats.bestScore);
            }
        } catch (error) {
            console.error('Error saving game completion:', error);
        }
    }

    async loadStats() {
        try {
            const response = await fetch('/api/stats');
            if (response.ok) {
                const stats = await response.json();
                this.updateBestScore(stats.bestScore);
            }
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }

    updateBestScore(score) {
        const bestScoreElement = document.getElementById('best-score');
        bestScoreElement.textContent = score !== null ? score : '-';
    }

    showWinModal() {
        document.getElementById('win-modal').classList.add('active');
    }

    hideWinModal() {
        document.getElementById('win-modal').classList.remove('active');
    }

    resetGame() {
        this.moves = 0;
        this.matchedPairs = 0;
        this.flippedCards = [];
        this.seconds = 0;
        this.isProcessing = false;

        this.updateMoves();
        this.updateTimer();
        this.createBoard();
        this.startTimer();
    }

    resetStats() {
        if (confirm('Are you sure you want to reset all statistics?')) {
            this.updateBestScore(null);
            // In a real implementation, you would also reset server-side stats
            alert('Statistics reset! (Note: Server stats are not reset in this demo)');
        }
    }

    startTimer() {
        this.stopTimer();
        this.timerInterval = setInterval(() => {
            this.seconds++;
            this.updateTimer();
        }, 1000);
    }

    stopTimer() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }

    updateMoves() {
        document.getElementById('moves').textContent = this.moves;
    }

    updateTimer() {
        document.getElementById('timer').textContent = this.formatTime(this.seconds);
    }

    formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${minutes}:${secs.toString().padStart(2, '0')}`;
    }

    shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }
}

// Initialize the game when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new MemoryGame();
});
