const canvas = document.getElementById("myCanvas");
const ctx = canvas.getContext("2d");

let score = 0;
let isStart = false;
const speed = 4;

// bricks
const brickRowCount = 3;
const brickColumnCount = 5;
const brickWidth = 75;
const brickHeight = 20;
const brickPadding = 10;
const brickOffsetTop = 30;
const brickOffsetLeft = 30;

var bricks = [];
for(var c=0; c<brickColumnCount; c++)
{
    bricks[c] = [];
    for(var r=0; r<brickRowCount; r++)
    {
        bricks[c][r] = { x: 0, y: 0, status: 1 };
    }
}


//keyboardInput
let rightPressed = false;
let leftPressed = false;

let x = canvas.width / 2;
let y = canvas.height - 30;
let dx = speed;
let dy = -speed;
const ballRadius = 10;

const paddleHeight = 10;
const paddleWidth = 75;
let paddleX = (canvas.width - paddleWidth) / 2;

// drawings of all items
function drawBall()
{
    ctx.beginPath();
    ctx.arc(x, y, ballRadius, 0, Math.PI * 2);
    ctx.fillStyle = "#0095DD";
    ctx.fill();
    ctx.closePath();
}

function drawPaddle()
{
    ctx.beginPath();
    ctx.rect(paddleX, canvas.height - paddleHeight - 10, paddleWidth, paddleHeight);
    ctx.fillStyle = "#0095DD";
    ctx.fill();
    ctx.closePath();
}

function drawBricks()
{
    for(var c=0; c<brickColumnCount; c++) 
    {
        for(var r=0; r<brickRowCount; r++)
        {
            if (bricks[c][r].status == 1)
            {
                var brickX = (c*(brickWidth+brickPadding))+brickOffsetLeft;
                var brickY = (r*(brickHeight+brickPadding))+brickOffsetTop;
                bricks[c][r].x = brickX;
                bricks[c][r].y = brickY;
                ctx.beginPath();
                ctx.rect(brickX, brickY, brickWidth, brickHeight);
                ctx.fillStyle = "#0095DD";
                ctx.fill();
                ctx.closePath();
            }
        }
    }
}

function drawScore()
{
    ctx.font = "16px Arial";
    ctx.fillStyle = "#0095DD";
    ctx.fillText(`Score: ${score}`, 8, 20)
}

function drawStart()
{
    ctx.font = "16px Arial";
    ctx.fillStyle = "#0095DD";
    ctx.fillText(`To start press Space`, canvas.width / 3, canvas.height / 2);
}

  


function draw()
{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    if (!isStart)
    {
        drawStart();
    }
    else
    {
        paddleCollisionDetector();
        brickCollisionDetection();
        drawBall();
        drawPaddle();
        drawBricks();
        drawScore();
    

        if (rightPressed) paddleX = Math.min(paddleX + 7, canvas.width - paddleWidth);
        else if (leftPressed) paddleX = Math.max(paddleX - 7, 0);
            
        
        x += dx;
        y += dy;
    }
}

// keyboardInput logic
document.addEventListener("keydown", keyDownHandler, false);
document.addEventListener("keyup", keyUpHandler, false);
// document.addEventListener("mousemove", mouseMoveHandler, false);

function keyDownHandler(e)
{
    if (e.key === "Right" || e.key === "ArrowRight")
        rightPressed = true;
    else if (e.key === "Left" || e.key === "ArrowLeft")
        leftPressed = true;
    else if (e.key == " " || e.code == "Space" || e.keyCode == 32)
        isStart = true;
}
  
function keyUpHandler(e)
{
    if (e.key === "Right" || e.key === "ArrowRight")
        rightPressed = false;
    else if (e.key === "Left" || e.key === "ArrowLeft")
        leftPressed = false;
}
// function mouseMoveHandler(e)
// {
//     const relativeX = e.clientX - canvas.offsetLeft;
//     if (relativeX > 0 && relativeX << canvas.width)
//         paddleX = relativeX - paddleWidth / 2;
// }


// collision logic
function brickCollisionDetection()
{
    for (let c = 0; c < brickColumnCount; c++)
    {
        for (let r = 0; r < brickRowCount; r++)
        {
            const b = bricks[c][r];
            if (b.status === 1) 
            {
                if (
                    x + ballRadius > b.x &&
                    x - ballRadius < b.x + brickWidth &&
                    y + ballRadius > b.y &&
                    y - ballRadius < b.y + brickHeight
                    )
                {
                    dy = -dy;
                    b.status = 0;
                    score ++;
                    if (score === brickRowCount * brickColumnCount)
                    {
                        alert("You win! Here is your medal");
                        document.location.reload();
                        clearInterval(interval);
                    }
                }
            }
        }
    }
}
  
function paddleCollisionDetector()
{
    if (x + dx > canvas.width - ballRadius || x + dx < ballRadius)
    {
        dx = -dx;
    }
      
    if (y + dy < ballRadius)
    {
        dy = -dy;
    }
    else if (y + dy > canvas.height - ballRadius - 15)
    {
        if (x > paddleX && x < paddleX + paddleWidth)
        {
            dy = -dy;
        } else if (y + dy > canvas.height - ballRadius)
        {
            alert("GAME OVER");
            document.location.reload();
            clearInterval(interval);
        }
    }
}
  


// frame rate change timer
const interval = setInterval(draw, 10);
