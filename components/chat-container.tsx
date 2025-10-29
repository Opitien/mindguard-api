"use client"

import { useState, useEffect, useRef, useOptimistic } from "react"
import type { Message } from "@/types/message"
import { ChatMessage } from "./chat-message"
import { ChatInput } from "./chat-input"
import { Avatar } from "@/components/ui/avatar"
import { Heart } from "lucide-react"

const INITIAL_MESSAGE: Message = {
  id: "1",
  role: "assistant",
  content: "Hi there 👋 I'm your emotional wellness assistant. How have you been feeling lately?",
  timestamp: new Date(),
}

export function ChatContainer() {
  const [messages, setMessages] = useState<Message[]>([INITIAL_MESSAGE])
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const [optimisticMessages, addOptimisticMessage] = useOptimistic(messages, (state, newMessage: Message) => [
    ...state,
    newMessage,
  ])

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [optimisticMessages, isTyping])

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content,
      timestamp: new Date(),
    }

    addOptimisticMessage(userMessage)
    setMessages((prev) => [...prev, userMessage])
    setIsTyping(true)

    try {
      // 🔥 Send text to your FastAPI backend
      const res = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: content }),
      })

      const data = await res.json()

      // Format bot reply nicely
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content:
          data?.label === "Depressed"
            ? `😔 Based on your message, you might be feeling **depressed**.\nConfidence: ${(data.probability * 100).toFixed(1)}%. Remember, you're not alone — reaching out for help is a strong step.`
            : `😊 You seem **not depressed** based on your message.\nConfidence: ${(data.probability * 100).toFixed(1)}%. Keep taking care of your mental health!`,
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, botMessage])
    } catch (error) {
      console.error("Error communicating with backend:", error)
      const errorMessage: Message = {
        id: (Date.now() + 2).toString(),
        role: "assistant",
        content: "⚠️ I couldn’t reach the backend right now. Please make sure your FastAPI server is running.",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsTyping(false)
    }
  }

  return (
    <div className="flex h-screen flex-col">
      {/* Header */}
      <header className="border-b border-border bg-card px-4 py-3 shadow-sm">
        <div className="mx-auto flex max-w-4xl items-center gap-3">
          <Avatar className="h-10 w-10">
            <div className="flex h-full w-full items-center justify-center bg-primary text-primary-foreground">
              <Heart className="h-5 w-5" />
            </div>
          </Avatar>
          <div>
            <h1 className="text-sm font-semibold text-foreground">Emotional Wellness Assistant</h1>
            <p className="text-xs text-muted-foreground">Here to listen and support you</p>
          </div>
        </div>
      </header>

      {/* Messages Area */}
      <main className="flex-1 overflow-y-auto px-4 py-6">
        <div className="mx-auto flex max-w-4xl flex-col gap-6">
          {optimisticMessages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
          {isTyping && (
            <ChatMessage
              message={{
                id: "typing",
                role: "assistant",
                content: "",
                timestamp: new Date(),
              }}
              isTyping
              typingText="Analyzing your message..."
            />
          )}
          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Input Area */}
      <ChatInput onSendMessage={handleSendMessage} disabled={isTyping} />
    </div>
  )
}
