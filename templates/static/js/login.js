var btn = document.getElementById('btn')
var btnAluno = document.getElementById('btnAluno')
var btnProfessor = document.getElementById('btnProfessor')

function leftClick() {
    btn.style.left = '2%'
    btn.style.width = '105px'
    btnAluno.style.color = 'white'
    btnProfessor.style.color = 'black'
}

function rightClick() {
    btn.style.left = '115px'
    btn.style.width = '135px'
    btnAluno.style.color = 'black'
    btnProfessor.style.color = 'white'
}