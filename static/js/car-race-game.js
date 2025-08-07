/**
 * Simple Car Race Game
 * A basic 2D car racing game where the player controls a car to avoid obstacles
 */

class CarRaceGame {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.gameWidth = this.canvas.width;
        this.gameHeight = this.canvas.height;
        
        // Game state
        this.gameRunning = false;
        this.gamePaused = false;
        this.score = 0;
        this.speed = 1;
        this.lives = 3;
        
        // Player car
        this.player = {
            x: this.gameWidth / 2 - 20,
            y: this.gameHeight - 80,
            width: 40,
            height: 60,
            speed: 5,
            color: '#4a90e2'
        };
        
        // Obstacles (enemy cars)
        this.obstacles = [];
        this.obstacleSpawnRate = 0.02;
        
        // Road properties
        this.roadLines = [];
        this.roadLineSpeed = 2;
        
        // Input handling
        this.keys = {};
        
        this.initializeControls();
        this.initializeRoadLines();
        this.bindEvents();
    }
    
    initializeControls() {
        const startBtn = document.getElementById('startBtn');
        const pauseBtn = document.getElementById('pauseBtn');
        const restartBtn = document.getElementById('restartBtn');
        const playAgainBtn = document.getElementById('playAgainBtn');
        
        startBtn.addEventListener('click', () => this.startGame());
        pauseBtn.addEventListener('click', () => this.togglePause());
        restartBtn.addEventListener('click', () => this.restartGame());
        playAgainBtn.addEventListener('click', () => this.restartGame());
    }
    
    initializeRoadLines() {
        // Create road lane lines
        for (let i = 0; i < this.gameHeight / 40; i++) {
            this.roadLines.push({
                x: this.gameWidth / 2,
                y: i * 40,
                width: 4,
                height: 20
            });
        }
    }
    
    bindEvents() {
        // Keyboard event listeners
        document.addEventListener('keydown', (e) => {
            this.keys[e.code] = true;
            e.preventDefault();
        });
        
        document.addEventListener('keyup', (e) => {
            this.keys[e.code] = false;
            e.preventDefault();
        });
    }
    
    startGame() {
        this.gameRunning = true;
        this.gamePaused = false;
        document.getElementById('startBtn').style.display = 'none';
        document.getElementById('pauseBtn').style.display = 'inline-block';
        document.getElementById('restartBtn').style.display = 'inline-block';
        document.getElementById('gameOverScreen').style.display = 'none';
        
        this.gameLoop();
    }
    
    togglePause() {
        this.gamePaused = !this.gamePaused;
        const pauseBtn = document.getElementById('pauseBtn');
        pauseBtn.textContent = this.gamePaused ? 'Resume' : 'Pause';
    }
    
    restartGame() {
        this.gameRunning = false;
        this.gamePaused = false;
        this.score = 0;
        this.speed = 1;
        this.lives = 3;
        this.obstacles = [];
        
        // Reset player position
        this.player.x = this.gameWidth / 2 - 20;
        this.player.y = this.gameHeight - 80;
        
        // Reset UI
        this.updateUI();
        document.getElementById('startBtn').style.display = 'inline-block';
        document.getElementById('pauseBtn').style.display = 'none';
        document.getElementById('restartBtn').style.display = 'none';
        document.getElementById('gameOverScreen').style.display = 'none';
        
        // Clear canvas
        this.ctx.clearRect(0, 0, this.gameWidth, this.gameHeight);
        this.drawBackground();
        this.drawPlayer();
    }
    
    gameLoop() {
        if (!this.gameRunning) return;
        
        if (!this.gamePaused) {
            this.update();
            this.draw();
        }
        
        requestAnimationFrame(() => this.gameLoop());
    }
    
    update() {
        // Handle player input
        this.handleInput();
        
        // Update obstacles
        this.updateObstacles();
        
        // Check collisions
        this.checkCollisions();
        
        // Update score and speed
        this.score += 1;
        this.speed = 1 + Math.floor(this.score / 1000) * 0.5;
        
        // Update UI
        this.updateUI();
    }
    
    handleInput() {
        // Move player car left/right
        if ((this.keys['ArrowLeft'] || this.keys['KeyA']) && this.player.x > 50) {
            this.player.x -= this.player.speed;
        }
        if ((this.keys['ArrowRight'] || this.keys['KeyD']) && this.player.x < this.gameWidth - this.player.width - 50) {
            this.player.x += this.player.speed;
        }
    }
    
    updateObstacles() {
        // Spawn new obstacles
        if (Math.random() < this.obstacleSpawnRate * this.speed) {
            this.spawnObstacle();
        }
        
        // Move obstacles down
        for (let i = this.obstacles.length - 1; i >= 0; i--) {
            const obstacle = this.obstacles[i];
            obstacle.y += obstacle.speed * this.speed;
            
            // Remove obstacles that are off screen
            if (obstacle.y > this.gameHeight) {
                this.obstacles.splice(i, 1);
            }
        }
        
        // Update road lines
        for (const line of this.roadLines) {
            line.y += this.roadLineSpeed * this.speed;
            if (line.y > this.gameHeight) {
                line.y = -20;
            }
        }
    }
    
    spawnObstacle() {
        const lanes = [100, 180, 260]; // Three lanes
        const lane = lanes[Math.floor(Math.random() * lanes.length)];
        
        this.obstacles.push({
            x: lane,
            y: -60,
            width: 40,
            height: 60,
            speed: 3 + Math.random() * 2,
            color: '#e74c3c'
        });
    }
    
    checkCollisions() {
        for (const obstacle of this.obstacles) {
            if (this.isColliding(this.player, obstacle)) {
                this.handleCollision();
                break;
            }
        }
    }
    
    isColliding(rect1, rect2) {
        return rect1.x < rect2.x + rect2.width &&
               rect1.x + rect1.width > rect2.x &&
               rect1.y < rect2.y + rect2.height &&
               rect1.y + rect1.height > rect2.y;
    }
    
    handleCollision() {
        this.lives--;
        
        if (this.lives <= 0) {
            this.gameOver();
        } else {
            // Brief invincibility period
            this.player.x = this.gameWidth / 2 - 20;
            this.obstacles = this.obstacles.filter(obstacle => 
                !this.isColliding(this.player, obstacle)
            );
        }
    }
    
    gameOver() {
        this.gameRunning = false;
        document.getElementById('finalScore').textContent = this.score;
        document.getElementById('gameOverScreen').style.display = 'block';
        document.getElementById('pauseBtn').style.display = 'none';
        document.getElementById('restartBtn').style.display = 'none';
    }
    
    draw() {
        this.ctx.clearRect(0, 0, this.gameWidth, this.gameHeight);
        
        this.drawBackground();
        this.drawRoadLines();
        this.drawPlayer();
        this.drawObstacles();
    }
    
    drawBackground() {
        // Draw road
        this.ctx.fillStyle = '#2c3e50';
        this.ctx.fillRect(0, 0, this.gameWidth, this.gameHeight);
        
        // Draw road sides
        this.ctx.fillStyle = '#27ae60';
        this.ctx.fillRect(0, 0, 50, this.gameHeight);
        this.ctx.fillRect(this.gameWidth - 50, 0, 50, this.gameHeight);
        
        // Draw road markings
        this.ctx.fillStyle = '#f39c12';
        this.ctx.fillRect(50, 0, 10, this.gameHeight);
        this.ctx.fillRect(this.gameWidth - 60, 0, 10, this.gameHeight);
    }
    
    drawRoadLines() {
        this.ctx.fillStyle = '#ecf0f1';
        for (const line of this.roadLines) {
            this.ctx.fillRect(line.x - line.width / 2, line.y, line.width, line.height);
        }
    }
    
    drawPlayer() {
        this.drawCar(this.player.x, this.player.y, this.player.width, this.player.height, this.player.color);
    }
    
    drawObstacles() {
        for (const obstacle of this.obstacles) {
            this.drawCar(obstacle.x, obstacle.y, obstacle.width, obstacle.height, obstacle.color);
        }
    }
    
    drawCar(x, y, width, height, color) {
        // Car body
        this.ctx.fillStyle = color;
        this.ctx.fillRect(x, y, width, height);
        
        // Car windows
        this.ctx.fillStyle = '#34495e';
        this.ctx.fillRect(x + 5, y + 5, width - 10, height / 3);
        this.ctx.fillRect(x + 5, y + height * 2/3 - 5, width - 10, height / 4);
        
        // Car wheels
        this.ctx.fillStyle = '#2c3e50';
        this.ctx.fillRect(x - 3, y + 10, 6, 12);
        this.ctx.fillRect(x + width - 3, y + 10, 6, 12);
        this.ctx.fillRect(x - 3, y + height - 22, 6, 12);
        this.ctx.fillRect(x + width - 3, y + height - 22, 6, 12);
    }
    
    updateUI() {
        document.getElementById('scoreDisplay').textContent = this.score;
        document.getElementById('speedDisplay').textContent = this.speed.toFixed(1);
        document.getElementById('livesDisplay').textContent = this.lives;
    }
}

// Initialize the game when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize the game if we're on the game page
    if (document.getElementById('gameCanvas')) {
        const game = new CarRaceGame();
        
        // Draw initial state
        game.drawBackground();
        game.drawPlayer();
    }
});