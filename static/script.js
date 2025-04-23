document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const themeToggle = document.getElementById('theme-toggle');

    // --- Theme Management ---
    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
    }

    // Check for saved theme preference or respect OS preference
    const savedTheme = localStorage.getItem('theme');
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    
    if (savedTheme) {
        setTheme(savedTheme);
    } else if (prefersDarkScheme.matches) {
        setTheme('dark');
    } else {
        setTheme('light');
    }

    // Toggle theme when button is clicked
    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        setTheme(currentTheme === 'dark' ? 'light' : 'dark');
    });

    // --- Session Management ---
    let sessionId = sessionStorage.getItem('virraChatSessionId');
    // if (!sessionId) {
    //     // If no session ID, the backend will create one on the first message
    //     console.log("No session ID found in sessionStorage. New session will be created on first message.");
    // }

    // --- Helper Functions ---
    // Function to detect and format JSON/code blocks in text
    function formatMessage(text) {
        // Check for code blocks with ```json or ```
        const codeBlockRegex = /```(json)?\s*([\s\S]*?)```/g;
        let formattedText = text;
        let match;
        
        // Replace code blocks with formatted HTML
        while ((match = codeBlockRegex.exec(text)) !== null) {
            const language = match[1] || '';
            let code = match[2].trim();
            let formattedCode = '';
            
            if (language.toLowerCase() === 'json') {
                try {
                    // Parse the JSON and format it with syntax highlighting
                    formattedCode = formatJSON(code);
                } catch (e) {
                    // If JSON parsing fails, just display as plain code
                    formattedCode = `<pre>${escapeHTML(code)}</pre>`;
                }
            } else {
                // For non-JSON code blocks, just escape HTML entities
                formattedCode = `<pre>${escapeHTML(code)}</pre>`;
            }
            
            // Create a code block container with language label and copy button
            const codeBlockHTML = `
                <div class="code-block ${language}">
                    ${language ? `<span class="code-block-label">${language}</span>` : ''}
                    <button class="copy-code-btn" title="Copy code">Copy</button>
                    ${formattedCode}
                </div>
            `;
            
            formattedText = formattedText.replace(match[0], codeBlockHTML);
        }
        
        // Also check for standalone JSON objects that aren't in code blocks
        // This is a simple heuristic and might need refinement
        if (!codeBlockRegex.test(text) && text.trim().startsWith('{') && text.trim().endsWith('}')) {
            try {
                const jsonObj = JSON.parse(text.trim());
                // If it's valid JSON, format it
                formattedText = `
                    <div class="code-block json">
                        <span class="code-block-label">json</span>
                        <button class="copy-code-btn" title="Copy code">Copy</button>
                        ${formatJSON(JSON.stringify(jsonObj, null, 2))}
                    </div>
                `;
            } catch (e) {
                // Not valid JSON, leave as is
                formattedText = text.replace(/\n/g, '<br>');
            }
        } else {
            // Handle normal line breaks for non-code text
            formattedText = formattedText.replace(/\n/g, '<br>');
        }
        
        return formattedText;
    }
    
    // Helper function to escape HTML entities
    function escapeHTML(text) {
        return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
    
    // Helper function to format JSON with syntax highlighting
    function formatJSON(json) {
        if (typeof json === 'string') {
            try {
                json = JSON.parse(json);
            } catch (e) {
                // If it's not valid JSON, try to format it as a string
                return highlightJSONString(json);
            }
        }
        
        // Convert back to a formatted string
        let formattedJSON = JSON.stringify(json, null, 2);
        
        // Apply syntax highlighting
        return highlightJSONString(formattedJSON);
    }
    
    function highlightJSONString(jsonString) {
        return jsonString
            .replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
                let cls = 'number';
                if (/^"/.test(match)) {
                    if (/:$/.test(match)) {
                        cls = 'key';
                        // Remove the colon from the key
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

    function addMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(sender === 'user' ? 'user-message' : 'bot-message');

        const messageP = document.createElement('p');
        // Format the message (handle JSON, code blocks, and line breaks)
        messageP.innerHTML = sender === 'bot' ? formatMessage(text) : text.replace(/\n/g, '<br>');

        messageDiv.appendChild(messageP);
        chatBox.appendChild(messageDiv);
        
        // Add event listeners to copy buttons if they exist
        const copyButtons = messageDiv.querySelectorAll('.copy-code-btn');
        copyButtons.forEach(btn => {
            btn.addEventListener('click', function() {
                const codeBlock = this.closest('.code-block');
                const code = codeBlock.querySelector('pre').textContent;
                navigator.clipboard.writeText(code).then(() => {
                    // Show feedback that code was copied
                    const originalText = this.textContent;
                    this.textContent = 'Copied!';
                    setTimeout(() => {
                        this.textContent = originalText;
                    }, 2000);
                });
            });
        });
        
        // Scroll to the bottom
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function showLoading(isLoading) {
        let loadingIndicator = document.getElementById('loading-indicator');
        if (isLoading) {
            if (!loadingIndicator) {
                // Create the container div for the message
                loadingIndicator = document.createElement('div');
                loadingIndicator.id = 'loading-indicator';
                loadingIndicator.classList.add('message', 'loading-indicator'); // Use message class for alignment

                // Create the paragraph element inside
                const loadingP = document.createElement('p');
                loadingP.textContent = 'Dr. Reed is thinking...'; 
                
                loadingIndicator.appendChild(loadingP);
                chatBox.appendChild(loadingIndicator);
                chatBox.scrollTop = chatBox.scrollHeight;
            }
            sendButton.disabled = true;
            userInput.disabled = true;
        } else {
            if (loadingIndicator) {
                loadingIndicator.remove();
            }
            sendButton.disabled = false;
            userInput.disabled = false;
            userInput.focus(); // Focus back on input after response
        }
    }

    // --- Event Handlers ---
    async function handleSendMessage() {
        const messageText = userInput.value.trim();
        if (!messageText) return;

        // Display user message immediately
        addMessage('user', messageText);
        userInput.value = ''; // Clear input field
        userInput.style.height = 'auto'; // Reset height after clearing
        userInput.style.height = userInput.scrollHeight + 'px'; // Adjust if needed

        showLoading(true);

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    session_id: sessionId, // Send current session ID (null if first message)
                    message: messageText 
                }),
            });

            showLoading(false);

            if (!response.ok) {
                // Try to get error message from response body
                let errorDetail = `HTTP error! status: ${response.status}`;
                try {
                    const errorData = await response.json();
                    errorDetail = errorData.detail || errorDetail;
                } catch (e) {
                    // Ignore if response is not JSON
                }
                addMessage('bot', `Sorry, an error occurred: ${errorDetail}`);
                console.error('Chat API error:', errorDetail);
                return;
            }

            const data = await response.json();
            
            // Update session ID if it was newly created or changed
            if (data.session_id && data.session_id !== sessionId) {
                sessionId = data.session_id;
                sessionStorage.setItem('virraChatSessionId', sessionId);
                console.log("Updated session ID:", sessionId);
            }

            addMessage('bot', data.response);

        } catch (error) {
            showLoading(false);
            addMessage('bot', 'Sorry, something went wrong while connecting to the server.');
            console.error('Error sending message:', error);
        }
    }

    // --- Auto-resize Textarea ---
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto'; // Reset height
        userInput.style.height = userInput.scrollHeight + 'px'; // Set to content height
    });

    // --- Event Listeners ---
    sendButton.addEventListener('click', handleSendMessage);

    userInput.addEventListener('keypress', (event) => {
        // Send message on Enter key press (Shift+Enter for newline)
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault(); // Prevent default Enter behavior (newline)
            handleSendMessage();
        }
    });
}); 