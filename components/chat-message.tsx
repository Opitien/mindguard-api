"use client"

import type { Message } from "@/types/message"
import { cn } from "../lib/utils"
import { useEffect, useState } from "react"

interface ChatMessageProps {
  message: Message
  isTyping?: boolean
  typingText?: string
}

export function ChatMessage({
  message,
  isTyping = false,
  typingText = "Typing",
}: ChatMessageProps) {
  const [isVisible, setIsVisible] = useState(false)
  const isUser = message.role === "user"

  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), 10)
    return () => clearTimeout(timer)
  }, [])

  const formatTime = (date: Date) =>
    date.toLocaleTimeString("en-US", {
      hour: "numeric",
      minute: "2-digit",
      hour12: true,
    })

  return (
    <div
      className={cn(
        "flex w-full gap-3 transition-all duration-500 ease-out",
        isUser ? "justify-end" : "justify-start",
        isVisible ? "translate-y-0 opacity-100" : "translate-y-4 opacity-0"
      )}
    >
      <div
        className={cn(
          "flex max-w-[80%] flex-col gap-1 md:max-w-[70%]",
          isUser ? "items-end" : "items-start"
        )}
      >
        <div
          className={cn(
            "rounded-2xl px-4 py-3 shadow-sm",
            isUser
              ? "bg-user-message text-user-message-foreground"
              : "bg-bot-message text-bot-message-foreground"
          )}
        >
          {isTyping ? (
            <div className="flex items-center gap-2">
              <div className="flex items-center gap-1">
                <span className="animate-bounce animation-delay-0 h-2 w-2 rounded-full bg-muted-foreground" />
                <span className="animate-bounce animation-delay-150 h-2 w-2 rounded-full bg-muted-foreground" />
                <span className="animate-bounce animation-delay-300 h-2 w-2 rounded-full bg-muted-foreground" />
              </div>
              <span className="text-xs text-muted-foreground">{typingText}</span>
            </div>
          ) : (
            <p className="whitespace-pre-wrap break-words text-sm leading-relaxed">
              {message.content}
            </p>
          )}
        </div>
        {!isTyping && (
          <span className="px-2 text-xs text-muted-foreground">
            {formatTime(message.timestamp)}
          </span>
        )}
      </div>
    </div>
  )
}
