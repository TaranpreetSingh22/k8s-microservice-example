import React, { useState } from 'react'

const API_BASE = {
  fib: 'http://fib-service:8000',
  prime: 'http://prime-service:8000',
  fact: 'http://fact-service:8000',
  pal: 'http://pal-service:8000'
}

export default function App() {
  const [n, setN] = useState('10')
  const [text, setText] = useState('madam')
  const [out, setOut] = useState('')

  async function callFib() {
    const res = await fetch(`${API_BASE.fib}/fibonacci/${encodeURIComponent(n)}`)
    setOut(await res.json())
  }
  async function callPrime() {
    const res = await fetch(`${API_BASE.prime}/is_prime/${encodeURIComponent(n)}`)
    setOut(await res.json())
  }
  async function callFact() {
    const res = await fetch(`${API_BASE.fact}/factorial/${encodeURIComponent(n)}`)
    setOut(await res.json())
  }
  async function callPal() {
    const res = await fetch(`${API_BASE.pal}/is_palindrome/${encodeURIComponent(text)}`)
    setOut(await res.json())
  }

  return (
    <div style={{padding:20,fontFamily:'system-ui,Segoe UI'}}>
      <h2>Algorithm microservices demo</h2>
      <div style={{marginBottom:12}}>
        <label>Number: <input value={n} onChange={e=>setN(e.target.value)} /></label>
        <button onClick={callFib} style={{marginLeft:8}}>Fibonacci</button>
        <button onClick={callPrime} style={{marginLeft:8}}>Is Prime?</button>
        <button onClick={callFact} style={{marginLeft:8}}>Factorial</button>
      </div>

      <div style={{marginBottom:12}}>
        <label>Text: <input value={text} onChange={e=>setText(e.target.value)} /></label>
        <button onClick={callPal} style={{marginLeft:8}}>Palindrome?</button>
      </div>

      <pre style={{whiteSpace:'pre-wrap', background:'#f6f8fa', padding:12}}>{JSON.stringify(out, null, 2)}</pre>
    </div>
  )
}
