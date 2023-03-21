const pickEl = document.querySelector('.pick-el')
const rockBtn = document.querySelector('.rock-btn')
const paperBtn = document.querySelector('.paper-btn')
const sciBtn = document.querySelector('.scissor-btn')
const confirmEl = document.querySelector('.confirm-el')
const vsEl = document.querySelector('.vs-el')
const resultEl = document.querySelector('.result-el')
const retryEl = document.querySelector('.retry-el')
let choice

function randomPick() {
  let comPick = Math.floor(Math.random() * 3)
  switch (comPick) {
    case 0:
      choice = 'ROCK'
      break
    case 1:
      choice = 'SCISSORS'
      break
    case 2:
      choice = 'PAPER'
      break
  }
}

function confirmPick(rps) {
  pickEl.textContent = `PICK ONE: YOUR PICK IS ${rps}`
  confirmEl.innerHTML = `
  <button class= 'confirm-btn'>CONFIRM SELECTION</button>
  `

  const confirmBtn = document.querySelector('.confirm-btn')
  confirmBtn.addEventListener('click', () => {
    randomPick()
    fight(rps, choice)})
}

function logic(onePick, twoPick) {
  if (onePick == twoPick) {
    resultEl.textContent = 'DRAW'
  } else if (onePick.length == 4 && twoPick.length == 5) {
    resultEl.textContent = 'YOU LOSE'
  } else if (onePick.length == 5 && twoPick.length == 8) {
    resultEl.textContent = 'YOU LOSE'
  } else if (onePick.length == 8 && twoPick.length == 5) {
    resultEl.textContent = 'YOU WIN'
  } else if (onePick.length == 5 && twoPick.length == 4) {
    resultEl.textContent = 'YOU WIN'
  } else if (onePick.length == 4 && twoPick.length == 8) {
    resultEl.textContent = 'YOU WIN'
  } else if (onePick.length == 8 && twoPick.length == 4) {
    resultEl.textContent = 'YOU LOSE'
  }
  retryEl.innerHTML = `
  <button class= 'retry-btn'>DO YOU WANT TO TRY AGAIN ?</button>
  `
  let retryBtn = document.querySelector('.retry-btn')
  retryBtn.addEventListener('click', () => reset())
}

function reset() {
  pickEl.textContent = 'PICK ONE'
  confirmEl.innerHTML = ''
  vsEl.innerHTML = ''
  resultEl.innerHTML = ''
  retryEl.innerHTML = ''
  randomPick()
}

function fight(playerPick, compPick) {
  vsEl.textContent = `${playerPick} VS ${compPick}`
  logic(playerPick, compPick)
}

rockBtn.addEventListener('click', () => confirmPick('ROCK'))
paperBtn.addEventListener('click', () => confirmPick('PAPER'))
sciBtn.addEventListener('click', () => confirmPick('SCISSORS'))
