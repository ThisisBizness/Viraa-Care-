document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const themeToggle = document.getElementById('theme-toggle');
    const typingIndicator = document.getElementById('typing-indicator');
    const charCount = document.getElementById('char-count');

    // --- Theme Management ---
    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
    }

    // Initialize theme
    const savedTheme = localStorage.getItem('theme');
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    
    if (savedTheme) {
        setTheme(savedTheme);
    } else if (prefersDarkScheme.matches) {
        setTheme('dark');
    } else {
        setTheme('light');
    }

    // Theme toggle event
    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        setTheme(currentTheme === 'dark' ? 'light' : 'dark');
    });

    // --- Session Management ---
    let sessionId = sessionStorage.getItem('viraaChatSessionId');

    // --- Character Count ---
    function updateCharCount() {
        const count = userInput.value.length;
        charCount.textContent = `${count}/1000`;
        
        // Enable/disable send button based on content
        sendButton.disabled = count === 0 || count > 1000;
    }

    userInput.addEventListener('input', updateCharCount);

    // --- Auto-resize Textarea ---
    function autoResizeTextarea() {
        userInput.style.height = 'auto';
        userInput.style.height = Math.min(userInput.scrollHeight, 120) + 'px';
    }

    userInput.addEventListener('input', autoResizeTextarea);

    // --- Message Formatting ---
    function formatMessage(text) {
        let formattedText = text;

        // Escape HTML first to prevent XSS and interference with Markdown
        formattedText = escapeHTML(formattedText);

        // Handle code blocks with ```language or ```
        const codeBlockRegex = /```(json|javascript|python|html|css|sql)?\s*([\s\S]*?)```/g;
        let codeMatches = [];
        let match;
        while ((match = codeBlockRegex.exec(formattedText)) !== null) {
            codeMatches.push({ placeholder: `__CODEBLOCK_${codeMatches.length}__`, content: match[0] });
        }
        codeMatches.forEach(m => formattedText = formattedText.replace(m.content, m.placeholder));

        // Handle bold text: **text**
        formattedText = formattedText.replace(/\*\*([\s\S]+?)\*\*/g, '<strong>$1</strong>');

        // Handle italic text: *text*
        formattedText = formattedText.replace(/\*([\s\S]+?)\*/g, '<em>$1</em>');
        
        // Handle paragraphs (double line breaks)
        // Replace deliberate double newlines (or more) with paragraph tags
        // Ensure that lists are not broken by this paragraph logic
        formattedText = formattedText.split(/\n\s*\n/).map(paragraph => {
            if (paragraph.trim().startsWith('-') || paragraph.trim().match(/^\d+\./)) {
                return paragraph; // Don't wrap list blocks in <p>
            }
            return paragraph.trim() ? `<p>${paragraph.trim().replace(/\n/g, '<br>')}</p>` : '';
        }).join('');

        // Handle unordered lists: - item or * item
        formattedText = formattedText.replace(/^\s*[-*]\s+(.*)/gm, '<ul><li>$1</li></ul>');
        formattedText = formattedText.replace(/<\/ul>\s*<ul>/g, ''); // Merge adjacent lists

        // Handle ordered lists: 1. item
        formattedText = formattedText.replace(/^\s*\d+\.\s+(.*)/gm, '<ol><li>$1</li></ol>');
        formattedText = formattedText.replace(/<\/ol>\s*<ol>/g, ''); // Merge adjacent lists
        
        // Restore code blocks
        codeMatches.forEach(m => {
            const langMatch = /```(json|javascript|python|html|css|sql)?\s*([\s\S]*?)```/.exec(m.content);
            const language = langMatch[1] || '';
            let code = langMatch[2].trim();
            let formattedCodeContent = '';

            if (language.toLowerCase() === 'json') {
                try {
                    const parsed = JSON.parse(code);
                    formattedCodeContent = formatJSON(JSON.stringify(parsed, null, 2));
                } catch (e) {
                    formattedCodeContent = `<pre>${code}</pre>`; // Already escaped
                }
            } else {
                formattedCodeContent = `<pre>${code}</pre>`; // Already escaped
            }
            
            const codeBlockHTML = `
                <div class="code-block ${language}">
                    ${language ? `<span class="code-block-label">${language}</span>` : ''}
                    <button class="copy-code-btn" title="Copy code">Copy</button>
                    ${formattedCodeContent}
                </div>
            `;
            formattedText = formattedText.replace(m.placeholder, codeBlockHTML);
        });
        
        // Fallback for any remaining single newlines if not part of <p> already
        // This is tricky because we don't want to add <br> inside <p> if already handled
        if (!formattedText.includes('<p>') && !formattedText.includes('<ul>') && !formattedText.includes('<ol>') && !formattedText.includes('<div class="code-block"')) {
             formattedText = formattedText.replace(/\n/g, '<br>');
        }

        return formattedText;
    }

    function escapeHTML(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function formatJSON(json) {
        if (typeof json === 'string') {
            try {
                json = JSON.parse(json);
            } catch (e) {
                return highlightJSONString(json);
            }
        }
        
        let formattedJSON = JSON.stringify(json, null, 2);
        return highlightJSONString(formattedJSON);
    }

    function highlightJSONString(jsonString) {
        return jsonString
            .replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
                let cls = 'number';
                if (/^"/.test(match)) {
                    if (/:$/.test(match)) {
                        cls = 'key';
                        match = match.replace(/:$/, '');
                    } else {
                        cls = 'string';
                    }
                } else if (/true|false/.test(match)) {
                    cls = 'boolean';
                } else if (/null/.test(match)) {
                    cls = 'null';
                }
                
                return '<span class="' + cls + '">' + escapeHTML(match) + '</span>';
            })
            .replace(/("[^"]*":)/g, '<span class="key">$1</span>');
    }

    // --- Message Management ---
    function getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    function createMessageHTML(sender, text, time = getCurrentTime()) {
        const isUser = sender === 'user';
        const senderName = isUser ? 'You' : 'Sona';
        const formattedText = isUser ? text.replace(/\n/g, '<br>') : formatMessage(text);
        
        return `
            <div class="message-group">
                <div class="message ${isUser ? 'user-message' : 'bot-message'}">
                    <div class="message-avatar">
                        <div class="avatar-circle">
                            ${isUser ? 
                                '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>' :
                                '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 3.5C14.5 3.3 14 3.9 14 4.4V5.5C14 6.3 13.3 7 12.5 7H11.5C10.7 7 10 6.3 10 5.5V4.4C10 3.9 9.5 3.3 9 3.5L3 7V9H5V20C5 20.6 5.4 21 6 21H8C8.6 21 9 20.6 9 20V14H15V20C15 20.6 15.4 21 16 21H18C18.6 21 19 20.6 19 20V9H21Z" fill="currentColor"/></svg>'
                            }
                        </div>
                    </div>
                    <div class="message-content">
                        <div class="message-header">
                            <span class="sender-name">${senderName}</span>
                            <span class="message-time">${time}</span>
                        </div>
                        <div class="message-text">
                            <p>${formattedText}</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    function addMessage(sender, text) {
        const messageHTML = createMessageHTML(sender, text);
        chatMessages.insertAdjacentHTML('beforeend', messageHTML);
        
        // Add copy button functionality to any new code blocks
        const newCodeBlocks = chatMessages.querySelectorAll('.message-group:last-child .copy-code-btn');
        newCodeBlocks.forEach(btn => {
            btn.addEventListener('click', handleCopyCode);
        });
        
        scrollToBottom();
    }

    function handleCopyCode(event) {
        const button = event.target;
        const codeBlock = button.closest('.code-block');
        const code = codeBlock.querySelector('pre').textContent;
        
        navigator.clipboard.writeText(code).then(() => {
            const originalText = button.textContent;
            button.textContent = 'Copied!';
            button.style.background = 'var(--color-success)';
            button.style.color = 'white';
            
            setTimeout(() => {
                button.textContent = originalText;
                button.style.background = '';
                button.style.color = '';
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy code:', err);
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = code;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            
            const originalText = button.textContent;
            button.textContent = 'Copied!';
            setTimeout(() => {
                button.textContent = originalText;
            }, 2000);
        });
    }

    function showTypingIndicator() {
        typingIndicator.style.display = 'block';
        scrollToBottom();
    }

    function hideTypingIndicator() {
        typingIndicator.style.display = 'none';
    }

    function scrollToBottom() {
        requestAnimationFrame(() => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        });
    }

    // --- Message Sending ---
    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message || sendButton.disabled) return;

        // Add user message immediately
        addMessage('user', message);
        
        // Clear input and show typing indicator
        userInput.value = '';
        updateCharCount();
        autoResizeTextarea();
        showTypingIndicator();
        
        // Disable send button
        sendButton.disabled = true;

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: sessionId,
                    message: message
                })
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Update session ID if we got a new one
            if (data.session_id && data.session_id !== sessionId) {
                sessionId = data.session_id;
                sessionStorage.setItem('viraaChatSessionId', sessionId);
            }

            // Hide typing indicator and add bot response
            hideTypingIndicator();
            addMessage('bot', data.response);

        } catch (error) {
            console.error('Error sending message:', error);
            
            hideTypingIndicator();
            
            // Show user-friendly error message
            const errorMessage = error.message.includes('Failed to fetch') 
                ? "I'm having trouble connecting right now. Please check your internet connection and try again."
                : `I apologize, but I encountered an error: ${error.message}. Please try again.`;
                
            addMessage('bot', errorMessage);
        } finally {
            // Re-enable send button if there's content
            updateCharCount();
        }
    }

    // --- Event Listeners ---
    sendButton.addEventListener('click', sendMessage);

    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            if (e.shiftKey) {
                // Allow new line with Shift+Enter
                return;
            } else {
                e.preventDefault();
                sendMessage();
            }
        }
    });

    // Prevent form submission on Enter
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
        }
    });

    // Focus on input when page loads
    userInput.focus();

    // Handle window resize
    window.addEventListener('resize', () => {
        scrollToBottom();
    });

    // --- Accessibility Enhancements ---
    
    // Add proper ARIA labels
    chatMessages.setAttribute('aria-live', 'polite');
    chatMessages.setAttribute('aria-label', 'Chat conversation');
    
    // Handle keyboard navigation
    document.addEventListener('keydown', (e) => {
        // Alt + T for theme toggle
        if (e.altKey && e.key === 't') {
            e.preventDefault();
            themeToggle.click();
        }
        
        // Escape to focus input
        if (e.key === 'Escape') {
            userInput.focus();
        }
    });

    // --- Initialize ---
    updateCharCount();
    scrollToBottom();
    
    console.log('Viraa Care chat interface initialized successfully');
}); 