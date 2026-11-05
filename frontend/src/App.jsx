import { useEffect, useRef, useState } from 'react'
import './App.css'

const API_URL = '/api/ask'

const TOPICS = [
  {
    group: 'Leave & time off',
    items: [
      'How many employees are female vs. male?',
      'How many employees are in the dataset?',
      'What is the average salary in Production?',
    ],
  },
  {
    group: 'Pay & benefits',
    items: [
      'When is salary credited each month?',
      'What health insurance benefits are available?',
      'How are reimbursements for travel claimed?',
    ],
  },
  {
    group: 'Hiring & onboarding',
    items: [
      'What documents does a new joiner need to submit?',
      'What is the probation period and review process?',
    ],
  },
  {
    group: 'Conduct & compliance',
    items: [
      'What is the remote work and attendance policy?',
      'How do I raise a workplace grievance?',
    ],
  },
]

const ICONS = {
  plus: 'M12 5v14M5 12h14',
  send: 'M5 12l14-7-5 14-2-5-7-2z',
  copy: 'M9 9h10v10H9zM5 15V5h10',
  menu: 'M4 7h16M4 12h16M4 17h16',
  close: 'M6 6l12 12M18 6L6 18',
  retry: 'M4 12a8 8 0 1 1 3 6.2M4 19v-5h5',
  check: 'M5 12l4 4 10-10',
  doc: 'M7 3h7l4 4v14H7zM14 3v4h4M10 12h5M10 16h5',
}

function Icon({ name, size = 18 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor"
      strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d={ICONS[name]} />
    </svg>
  )
}

function inline(text) {
  return text.split(/\*\*(.+?)\*\*/g).map((part, i) =>
    i % 2 ? <strong key={i}>{part}</strong> : part,
  )
}

function Answer({ text }) {
  const blocks = text.trim().split(/\n{2,}/)
  return blocks.map((block, i) => {
    const lines = block.split('\n').filter(Boolean)
    const isBullets = lines.every((l) => /^\s*[-*•]\s+/.test(l))
    const isNumbers = lines.every((l) => /^\s*\d+[.)]\s+/.test(l))
    if (isBullets || isNumbers) {
      const Tag = isNumbers ? 'ol' : 'ul'
      return (
        <Tag key={i}>
          {lines.map((l, j) => (
            <li key={j}>{inline(l.replace(/^\s*([-*•]|\d+[.)])\s+/, ''))}</li>
          ))}
        </Tag>
      )
    }
    return <p key={i}>{inline(lines.join(' '))}</p>
  })
}

const newChat = () => ({ id: crypto.randomUUID(), title: 'New conversation', messages: [] })

export default function App() {
  const [chats, setChats] = useState(() => [newChat()])
  const [activeId, setActiveId] = useState(chats[0].id)
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [topK, setTopK] = useState(5)
  const [drawer, setDrawer] = useState(false)
  const [copied, setCopied] = useState(null)
  const endRef = useRef(null)
  const inputRef = useRef(null)

  const chat = chats.find((c) => c.id === activeId)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [chat.messages.length, loading, activeId])

  const patchChat = (id, fn) =>
    setChats((all) => all.map((c) => (c.id === id ? fn(c) : c)))

  async function ask(question) {
    const q = question.trim()
    if (!q || loading) return
    const id = activeId
    const msgId = crypto.randomUUID()
    patchChat(id, (c) => ({
      ...c,
      title: c.messages.length ? c.title : q.slice(0, 48),
      messages: [...c.messages, { id: msgId, role: 'user', text: q, time: new Date() }],
    }))
    setInput('')
    setLoading(true)
    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q, top_k: topK }),
      })
      if (!res.ok) throw new Error(`The server returned ${res.status}.`)
      const data = await res.json()
      const text = data.answer || 'No answer was found in the HR knowledge base.'
      patchChat(id, (c) => ({
        ...c,
        messages: [...c.messages, { id: crypto.randomUUID(), role: 'assistant', text, time: new Date() }],
      }))
    } catch (err) {
      patchChat(id, (c) => ({
        ...c,
        messages: [...c.messages, {
          id: crypto.randomUUID(), role: 'assistant', error: true, question: q, time: new Date(),
          text: `Couldn’t reach the HR assistant. ${err.message} Check that the API is running, then try again.`,
        }],
      }))
    } finally {
      setLoading(false)
      inputRef.current?.focus()
    }
  }

  function startChat() {
    const c = newChat()
    setChats((all) => [c, ...all])
    setActiveId(c.id)
    setDrawer(false)
    inputRef.current?.focus()
  }

  function copy(m) {
    navigator.clipboard?.writeText(m.text)
    setCopied(m.id)
    setTimeout(() => setCopied(null), 1500)
  }

  const fmt = (d) => d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })

  return (
    <div className="shell">
      <aside className={`side ${drawer ? 'open' : ''}`}>
        <div className="brand">
          <span className="mark">HR</span>
          <div>
            <strong>PeopleDesk</strong>
            <small>HR knowledge assistant</small>
          </div>
          <button className="icon-btn only-mobile" onClick={() => setDrawer(false)} aria-label="Close menu">
            <Icon name="close" />
          </button>
        </div>

        <button className="new-chat" onClick={startChat}>
          <Icon name="plus" /> New conversation
        </button>

        <nav className="side-scroll" aria-label="Sidebar">
          <section>
            <h3>Recent</h3>
            <ul className="history">
              {chats.map((c) => (
                <li key={c.id}>
                  <button
                    className={c.id === activeId ? 'active' : ''}
                    onClick={() => { setActiveId(c.id); setDrawer(false) }}
                  >
                    {c.title}
                  </button>
                </li>
              ))}
            </ul>
          </section>

          <section>
            <h3>Common HR questions</h3>
            {TOPICS.map((t) => (
              <div className="topic" key={t.group}>
                <h4>{t.group}</h4>
                {t.items.map((q) => (
                  <button key={q} onClick={() => { setDrawer(false); ask(q) }}>{q}</button>
                ))}
              </div>
            ))}
          </section>
        </nav>

        <div className="settings">
          <label htmlFor="topk">
            Sources per answer <output>{topK}</output>
          </label>
          <input id="topk" type="range" min="1" max="10" value={topK}
            onChange={(e) => setTopK(+e.target.value)} />
          <p>More sources give broader answers but take longer.</p>
        </div>
      </aside>

      {drawer && <div className="scrim" onClick={() => setDrawer(false)} />}

      <main className="main">
        <header className="bar">
          <button className="icon-btn only-mobile" onClick={() => setDrawer(true)} aria-label="Open menu">
            <Icon name="menu" />
          </button>
          <div>
            <h1>HR Assistant</h1>
            <p>Answers come from your company’s HR policies and employee records.</p>
          </div>
          <span className="status"><i /> Connected</span>
        </header>

        <div className="thread" role="log" aria-live="polite">
          {chat.messages.length === 0 ? (
            <div className="empty">
              <span className="empty-icon"><Icon name="doc" size={26} /></span>
              <h2>What do you need to know?</h2>
              <p>Ask about leave, payroll, benefits, onboarding or company policy. Each answer is drawn from the HR documents your team has uploaded.</p>
              <div className="starters">
                {TOPICS.map((t) => (
                  <button key={t.group} onClick={() => ask(t.items[0])}>
                    <small>{t.group}</small>
                    {t.items[0]}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            chat.messages.map((m) => (
              <article key={m.id} className={`msg ${m.role} ${m.error ? 'error' : ''}`}>
                <span className="avatar">{m.role === 'user' ? 'You' : 'HR'}</span>
                <div className="bubble">
                  {m.role === 'user' ? <p>{m.text}</p> : m.error ? <p>{m.text}</p> : <Answer text={m.text} />}
                  <footer>
                    <time>{fmt(m.time)}</time>
                    {m.role === 'assistant' && !m.error && (
                      <button onClick={() => copy(m)}>
                        <Icon name={copied === m.id ? 'check' : 'copy'} size={14} />
                        {copied === m.id ? 'Copied' : 'Copy'}
                      </button>
                    )}
                    {m.error && (
                      <button onClick={() => ask(m.question)}>
                        <Icon name="retry" size={14} /> Try again
                      </button>
                    )}
                  </footer>
                </div>
              </article>
            ))
          )}

          {loading && (
            <article className="msg assistant">
              <span className="avatar">HR</span>
              <div className="bubble typing" aria-label="Searching HR documents">
                <span /><span /><span />
                <em>Searching HR documents…</em>
              </div>
            </article>
          )}
          <div ref={endRef} />
        </div>

        <form className="composer" onSubmit={(e) => { e.preventDefault(); ask(input) }}>
          <textarea
            ref={inputRef}
            rows={1}
            value={input}
            placeholder="Ask an HR question, e.g. “How much notice do I need to give?”"
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); ask(input) }
            }}
            aria-label="Your question"
          />
          <button type="submit" disabled={!input.trim() || loading}>
            <Icon name="send" /> Send
          </button>
        </form>
        <p className="fine">Answers are generated from company documents. Confirm important decisions with the HR team.</p>
      </main>
    </div>
  )
}