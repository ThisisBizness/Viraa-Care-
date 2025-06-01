document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const themeToggle = document.getElementById('theme-toggle');
    const typingIndicator = document.getElementById('typing-indicator');
    // Input area is no longer the primary interaction, but we might use it for displaying answers
    const mainContentArea = document.getElementById('chat-messages'); // Re-using this for display

    // Enhanced loading state management
    let isLoading = false;

    // --- Enhanced Theme Management ---
    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        // Update theme toggle aria-label
        const toggleLabel = theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme';
        themeToggle.setAttribute('aria-label', toggleLabel);
    }

    const savedTheme = localStorage.getItem('theme');
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    
    if (savedTheme) {
        setTheme(savedTheme);
    } else if (prefersDarkScheme.matches) {
        setTheme('dark');
    } else {
        setTheme('light');
    }

    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        setTheme(currentTheme === 'dark' ? 'light' : 'dark');
    });

    // Listen for system theme changes
    prefersDarkScheme.addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
            setTheme(e.matches ? 'dark' : 'light');
        }
    });

    // --- Session Management ---
    let sessionId = sessionStorage.getItem('viraaChatSessionId');
    let currentCategory = null; // Track current category for better navigation

    // --- Enhanced Categories and Questions Data ---
    const categories = [
        {
            name: "Is My Baby Getting Enough? / Is My Milk Okay?",
            icon: "🍼",
            questions: [
                "How can I tell if my baby is getting enough milk when I breastfeed?",
                "What are the sure signs my baby is well-fed and satisfied after breastfeeding?",
                "My baby fusses at the breast or pulls away. Could it be they're not getting enough milk?",
                "How does my body actually make enough milk for my baby?",
                "What is colostrum, and why is everyone saying it's so important for my newborn?",
                "What are the main benefits of my breast milk for my baby right now?",
                "My breasts don't feel as \"full\" as before, or they feel uneven after feeding. Is this a sign of a problem?",
                "I've heard breast milk changes. Does my milk change for my baby's needs, like at night or in the morning?"
            ]
        },
        {
            name: "Help! Breastfeeding is Painful!",
            icon: "😣",
            questions: [
                "Why are my nipples so sore? Is some pain just part of breastfeeding?",
                "How can I fix my baby's latch to stop it from hurting me?",
                "Is it normal to feel cramping in my belly when I breastfeed?",
                "What are the absolute \"must-do's\" before I even try to latch my baby to avoid problems?",
                "How do I hold my own breasts correctly to help my baby latch without pain?",
                "What does a \"good latch\" actually look like? I need to see it.",
                "If the pain doesn't stop, what are my options? Do I have to just give up?"
            ]
        },
        {
            name: "My Baby is Struggling to Latch!",
            icon: "👶",
            questions: [
                "My baby just can't seem to latch on properly. What are the key things to get right?",
                "How do I get my baby to open their mouth WIDE for a good latch?",
                "My baby seems to only get the very tip of my nipple. How do I encourage a deeper latch?",
                "What are the immediate signs I can look for to know if the latch is bad?",
                "How should I hold my baby (neck, body) to help them latch effectively?",
                "What is \"breast crawl\" and can my baby really find the breast on their own?",
                "What are the early signs (feeding cues) that my baby is ready to eat, even before they cry?",
                "If my baby is crying from hunger, will it be harder to latch them?"
            ]
        },
        {
            name: "I Need to Use a Bottle (Formula or My Milk)",
            icon: "🍼",
            questions: [
                "If I have to use formula, is it a bad choice for my baby?",
                "Can I give both breast milk and formula? How do I manage that?",
                "Can formula be hard for my baby to digest? What if they seem uncomfortable?",
                "What's the best way to give my baby a bottle to avoid problems? (Paced Bottle Feeding)",
                "How do I choose a good bottle and nipple if I'm also breastfeeding?",
                "Should I still hold my baby close and make eye contact when bottle-feeding?"
            ]
        },
        {
            name: "Taking Care of ME While Breastfeeding",
            icon: "💆‍♀️",
            questions: [
                "What should I eat when I'm breastfeeding? Are there foods I absolutely have to avoid?",
                "Will I be hungrier when breastfeeding, and how much more should I eat?",
                "Why is eating well important for me, not just for making milk?",
                "How much water should I be drinking?",
                "What's the most important \"non-food\" nutrition I need as a new breastfeeding mom?",
                "My family has a lot of old wives' tales about breastfeeding. How do I deal with these myths?",
                "How can my partner and family truly support me and this breastfeeding journey?"
            ]
        }
    ];

    // --- Enhanced UI Rendering with Better Accessibility ---
    function displayCategories() {
        currentCategory = null;
        const categoriesHTML = `
            <div class="selection-prompt" role="status" aria-live="polite">
                Please select a category to explore:
            </div>
            <nav aria-label="Question categories">
                <ul class="categories-list" role="list">
                    ${categories.map((category, index) => `
                        <li role="listitem">
                            <button class="category-button" 
                                    data-category-index="${index}"
                                    aria-describedby="category-${index}-desc">
                                <span class="category-icon" aria-hidden="true">${category.icon}</span>
                                <span class="category-text">${category.name}</span>
                            </button>
                            <div id="category-${index}-desc" class="sr-only">
                                Category with ${category.questions.length} questions
                            </div>
                        </li>
                    `).join('')}
                </ul>
            </nav>
        `;
        
        mainContentArea.innerHTML = categoriesHTML;
        addCategoryEventListeners();
        scrollToTop();
        announceToScreenReader('Categories loaded. Choose a category to see available questions.');
    }

    function displayQuestions(categoryIndex) {
        const category = categories[categoryIndex];
        currentCategory = categoryIndex;
        
        const questionsHTML = `
            <button class="back-button" id="back-to-categories" aria-label="Go back to categories">
                ← Back to Categories
            </button>
            <h2 class="category-title-display" id="category-title">
                <span aria-hidden="true">${category.icon}</span>
                ${category.name}
            </h2>
            <div class="selection-prompt" role="status" aria-live="polite">
                Choose a question from this category:
            </div>
            <nav aria-label="Questions in category" aria-describedby="category-title">
                <ul class="questions-list" role="list">
                    ${category.questions.map((questionText, index) => `
                        <li role="listitem">
                            <button class="question-button" 
                                    data-question-text="${escapeHTML(questionText)}"
                                    aria-describedby="question-${index}-desc">
                                ${questionText}
                            </button>
                            <div id="question-${index}-desc" class="sr-only">
                                Click to get AI-powered answer
                            </div>
                        </li>
                    `).join('')}
                </ul>
            </nav>
        `;
        
        mainContentArea.innerHTML = questionsHTML;
        addQuestionEventListeners();
        scrollToTop();
        announceToScreenReader(`${category.questions.length} questions loaded for ${category.name}`);
    }

    function addCategoryEventListeners() {
        const categoryButtons = document.querySelectorAll('.category-button');
        categoryButtons.forEach(button => {
            button.addEventListener('click', handleCategoryClick);
            button.addEventListener('keydown', handleKeyboardNavigation);
        });
    }

    function addQuestionEventListeners() {
        const questionButtons = document.querySelectorAll('.question-button');
        const backButton = document.getElementById('back-to-categories');
        
        questionButtons.forEach(button => {
            button.addEventListener('click', handleQuestionClick);
            button.addEventListener('keydown', handleKeyboardNavigation);
        });
        
        if (backButton) {
            backButton.addEventListener('click', displayCategories);
            backButton.addEventListener('keydown', handleKeyboardNavigation);
        }
    }

    function handleCategoryClick(event) {
        if (isLoading) return;
        const categoryIndex = parseInt(event.currentTarget.dataset.categoryIndex);
        displayQuestions(categoryIndex);
    }

    function handleQuestionClick(event) {
        if (isLoading) return;
        const questionText = event.currentTarget.dataset.questionText;
        fetchAnswer(questionText);
    }

    // Enhanced keyboard navigation
    function handleKeyboardNavigation(event) {
        const currentElement = event.target;
        const allButtons = [...document.querySelectorAll('.category-button, .question-button, .back-button')];
        const currentIndex = allButtons.indexOf(currentElement);

        switch (event.key) {
            case 'ArrowDown':
                event.preventDefault();
                if (currentIndex < allButtons.length - 1) {
                    allButtons[currentIndex + 1].focus();
                }
                break;
            case 'ArrowUp':
                event.preventDefault();
                if (currentIndex > 0) {
                    allButtons[currentIndex - 1].focus();
                }
                break;
            case 'Home':
                event.preventDefault();
                allButtons[0].focus();
                break;
            case 'End':
                event.preventDefault();
                allButtons[allButtons.length - 1].focus();
                break;
            case 'Enter':
            case ' ':
                event.preventDefault();
                currentElement.click();
                break;
        }
    }

    // Enhanced fetch with better error handling and loading states
    async function fetchAnswer(questionText) {
        if (isLoading) return;
        
        setLoadingState(true);
        mainContentArea.innerHTML = '';
        addMessageToUI('user', questionText);
        showTypingIndicator();

        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: sessionId,
                    message: questionText
                }),
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            if (data.session_id && data.session_id !== sessionId) {
                sessionId = data.session_id;
                sessionStorage.setItem('viraaChatSessionId', sessionId);
            }
            
            hideTypingIndicator();
            addMessageToUI('bot', data.response, true, data.media);
            announceToScreenReader('Answer received from Sona');
            
        } catch (error) {
            console.error('Error fetching answer:', error);
            hideTypingIndicator();
            
            let errorMessage;
            if (error.name === 'AbortError') {
                errorMessage = "The request timed out. Please try again with a shorter question or check your internet connection.";
            } else if (error.message.includes('Failed to fetch')) {
                errorMessage = "I'm having trouble connecting. Please check your internet connection and try again.";
            } else {
                errorMessage = `Sorry, an error occurred: ${error.message}. Please try again.`;
            }
            
            addMessageToUI('bot', errorMessage, true);
            announceToScreenReader('Error occurred while getting answer');
        } finally {
            setLoadingState(false);
        }
    }

    function setLoadingState(loading) {
        isLoading = loading;
        const buttons = document.querySelectorAll('.category-button, .question-button, .back-button');
        buttons.forEach(button => {
            button.disabled = loading;
            if (loading) {
                button.setAttribute('aria-busy', 'true');
            } else {
                button.removeAttribute('aria-busy');
            }
        });
    }

    // --- Enhanced Message Formatting & Display ---
    function announceToScreenReader(message) {
        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', 'polite');
        announcement.setAttribute('aria-atomic', 'true');
        announcement.className = 'sr-only';
        announcement.textContent = message;
        document.body.appendChild(announcement);
        
        setTimeout(() => {
            document.body.removeChild(announcement);
        }, 1000);
    }

    function formatMessage(text) {
        let formattedText = text;
        
        // Escape HTML first
        formattedText = escapeHTML(formattedText);
        
        // Handle code blocks first (preserve them)
        const codeBlockRegex = /```(json|javascript|python|html|css|sql|typescript|jsx|tsx)?\s*([\s\S]*?)```/g;
        let codeMatches = [];
        let match;
        
        while ((match = codeBlockRegex.exec(formattedText)) !== null) {
            codeMatches.push({ 
                placeholder: `__CODEBLOCK_${codeMatches.length}__`, 
                content: match[0],
                language: match[1] || '',
                code: match[2].trim()
            });
        }
        
        // Replace code blocks with placeholders
        codeMatches.forEach(m => {
            formattedText = formattedText.replace(m.content, m.placeholder);
        });
        
        // Handle headings (##, ###)
        formattedText = formattedText.replace(/^### (.*$)/gm, '<h3>$1</h3>');
        formattedText = formattedText.replace(/^## (.*$)/gm, '<h2>$1</h2>');
        formattedText = formattedText.replace(/^# (.*$)/gm, '<h1>$1</h1>');
        
        // Format text styling
        formattedText = formattedText.replace(/\*\*([\s\S]+?)\*\*/g, '<strong>$1</strong>');
        formattedText = formattedText.replace(/\*([\s\S]+?)\*/g, '<em>$1</em>');
        
        // Convert paragraphs while preserving headings
        const paragraphs = formattedText.split(/\n\s*\n/);
        formattedText = paragraphs.map(paragraph => {
            const trimmed = paragraph.trim();
            if (!trimmed) return '';
            
            // Skip if it's a heading, list, or already formatted
            if (trimmed.match(/^<h[1-6]>/) || 
                trimmed.startsWith('-') || 
                trimmed.match(/^\d+\./) ||
                trimmed.startsWith('<ul>') ||
                trimmed.startsWith('<ol>')) {
                return trimmed;
            }
            
            return `<p>${trimmed.replace(/\n/g, '<br>')}</p>`;
        }).join('\n');
        
        // Format lists with better handling
        // Handle bullet points
        formattedText = formattedText.replace(/(?:^|\n)(\s*[-*•]\s+[^\n]+(?:\n\s*[-*•]\s+[^\n]+)*)/gm, (match) => {
            const lines = match.trim().split('\n');
            const listItems = lines.map(line => {
                const content = line.replace(/^\s*[-*•]\s+/, '');
                return `<li>${content}</li>`;
            }).join('');
            return `<ul>${listItems}</ul>`;
        });
        
        // Handle numbered lists
        formattedText = formattedText.replace(/(?:^|\n)(\s*\d+\.\s+[^\n]+(?:\n\s*\d+\.\s+[^\n]+)*)/gm, (match) => {
            const lines = match.trim().split('\n');
            const listItems = lines.map(line => {
                const content = line.replace(/^\s*\d+\.\s+/, '');
                return `<li>${content}</li>`;
            }).join('');
            return `<ol>${listItems}</ol>`;
        });
        
        // Clean up consecutive list elements
        formattedText = formattedText.replace(/<\/ul>\s*<ul>/g, '');
        formattedText = formattedText.replace(/<\/ol>\s*<ol>/g, '');
        
        // Restore code blocks with enhanced formatting
        codeMatches.forEach(m => {
            const codeBlockHTML = `
                <div class="code-block ${m.language}" role="group" aria-label="Code example">
                    ${m.language ? `<div class="code-block-label" aria-label="Programming language">${m.language}</div>` : ''}
                    <button class="copy-code-btn" 
                            title="Copy code to clipboard" 
                            aria-label="Copy code to clipboard"
                            data-code="${escapeHTML(m.code)}">
                        <span aria-hidden="true">📋</span> Copy
                    </button>
                    <pre tabindex="0" role="text" aria-label="Code content">${m.language.toLowerCase() === 'json' ? formatJSON(m.code) : `<code>${m.code}</code>`}</pre>
                </div>
            `;
            formattedText = formattedText.replace(m.placeholder, codeBlockHTML);
        });
        
        // Clean up extra whitespace and newlines
        formattedText = formattedText.replace(/\n{3,}/g, '\n\n');
        formattedText = formattedText.replace(/^\s+|\s+$/g, '');
        
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
        return highlightJSONString(JSON.stringify(json, null, 2));
    }

    function highlightJSONString(jsonString) {
        return jsonString
            .replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
                let cls = 'number';
                if (/^"/.test(match)) { 
                    cls = /:$/.test(match) ? 'key' : 'string'; 
                    if(cls === 'key') match = match.replace(/:$/, '');
                }
                else if (/true|false/.test(match)) { cls = 'boolean'; }
                else if (/null/.test(match)) { cls = 'null'; }
                return '<span class="' + cls + '">' + escapeHTML(match) + '</span>';
            }).replace(/("[^"]*":)/g, '<span class="key">$1</span>');
    }

    function getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    function addMessageToUI(sender, text, isAnswerDisplay = false, media = null) {
        const time = getCurrentTime();
        const isUser = sender === 'user';
        const senderName = isUser ? 'You' : 'Sona';
        const formattedText = isUser ? escapeHTML(text) : formatMessage(text);

        const messageHTML = `
            <div class="message-group">
                <article class="message ${isUser ? 'user-message' : 'bot-message'} ${isAnswerDisplay ? 'answer-display' : ''}"
                         role="${isUser ? 'user' : 'assistant'}"
                         aria-label="${senderName} message">
                    <div class="message-avatar">
                        <div class="avatar-circle" aria-hidden="true">
                            ${isUser ?
                                '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>' :
                                '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 3.5C14.5 3.3 14 3.9 14 4.4V5.5C14 6.3 13.3 7 12.5 7H11.5C10.7 7 10 6.3 10 5.5V4.4C10 3.9 9.5 3.3 9 3.5L3 7V9H5V20C5 20.6 5.4 21 6 21H8C8.6 21 9 20.6 9 20V14H15V20C15 20.6 15.4 21 16 21H18C18.6 21 19 20.6 19 20V9H21Z" fill="currentColor"/></svg>'
                            }
                        </div>
                    </div>
                    <div class="message-content">
                        <div class="message-header">
                            <span class="sender-name">${senderName}</span>
                            <time class="message-time" datetime="${new Date().toISOString()}">${time}</time>
                        </div>
                        <div class="message-text" ${isAnswerDisplay ? 'role="main"' : ''}>
                            ${isAnswerDisplay ? formattedText : `<p>${formattedText}</p>`}
                            ${media && isAnswerDisplay && !isUser ? generateMediaHTML(media) : ''}
                            ${isAnswerDisplay ? `
                                <div class="answer-actions">
                                    <button class="back-button" 
                                            onclick="goBackToCategoriesOrQuestions()"
                                            aria-label="Go back to questions">
                                        ← Back to Questions
                                    </button>
                                </div>
                            ` : ''}
                        </div>
                    </div>
                </article>
            </div>
        `;
        
        if (isAnswerDisplay && sender === 'bot') {
            mainContentArea.innerHTML = messageHTML;
        } else {
            mainContentArea.insertAdjacentHTML('beforeend', messageHTML);
        }
        
        // Add event listeners for copy buttons
        const newCodeBlocks = mainContentArea.querySelectorAll('.message-group:last-child .copy-code-btn');
        newCodeBlocks.forEach(btn => btn.addEventListener('click', handleCopyCode));
        
        scrollToBottom();
    }

    function generateMediaHTML(media) {
        if (!media) return '';
        
        let mediaContent = '';
        
        // Generate video content
        if (media.video) {
            const videoHTML = `
                <video 
                    class="video-player" 
                    controls 
                    preload="metadata"
                    poster="${media.video.poster || ''}"
                    aria-label="Demonstration video"
                    onloadstart="handleMediaLoadStart(this)"
                    oncanplay="handleMediaCanPlay(this)"
                    onerror="handleMediaError(this)">
                    <source src="${media.video.url}" type="${media.video.type}">
                    <p>Your browser doesn't support video playback. <a href="${media.video.url}" target="_blank">Download the video</a> instead.</p>
                </video>
            `;
            
            mediaContent += `
                <div class="media-section">
                    <div class="media-header">
                        <svg class="media-icon" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M8 5v14l11-7z"/>
                        </svg>
                        <h3 class="media-title">Video Demonstration</h3>
                    </div>
                    <div class="media-content">
                        ${videoHTML}
                        <div class="media-controls">
                            <button class="media-control-btn" onclick="togglePlayPause(this.closest('.media-section').querySelector('video'))">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M8 5v14l11-7z"/>
                                </svg>
                                Play/Pause
                            </button>
                            <div class="media-info">
                                <span>Click to play the demonstration</span>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }
        
        // Generate audio content
        if (media.audio) {
            const audioHTML = `
                <audio 
                    class="audio-player" 
                    controls 
                    preload="metadata"
                    aria-label="Demonstration audio"
                    onloadstart="handleMediaLoadStart(this)"
                    oncanplay="handleMediaCanPlay(this)"
                    onerror="handleMediaError(this)">
                    <source src="${media.audio.url}" type="${media.audio.type}">
                    <p>Your browser doesn't support audio playback. <a href="${media.audio.url}" target="_blank">Download the audio</a> instead.</p>
                </audio>
            `;
            
            mediaContent += `
                <div class="media-section">
                    <div class="media-header">
                        <svg class="media-icon" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>
                        </svg>
                        <h3 class="media-title">Audio Guide</h3>
                    </div>
                    <div class="media-content">
                        ${audioHTML}
                        <div class="media-controls">
                            <button class="media-control-btn" onclick="togglePlayPause(this.closest('.media-section').querySelector('audio'))">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M8 5v14l11-7z"/>
                                </svg>
                                Play/Pause
                            </button>
                            <div class="media-info">
                                <span>Listen to the audio guide</span>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }
        
        if (mediaContent) {
            return `
                <div class="media-container">
                    ${mediaContent}
                </div>
            `;
        }
        
        return '';
    }

    // Media control functions
    window.togglePlayPause = function(mediaElement) {
        if (mediaElement.paused || mediaElement.ended) {
            mediaElement.play().catch(e => {
                console.error('Error playing media:', e);
                announceToScreenReader('Unable to play media');
            });
        } else {
            mediaElement.pause();
        }
    }

    window.handleMediaLoadStart = function(mediaElement) {
        const container = mediaElement.closest('.media-section');
        const info = container.querySelector('.media-info span');
        if (info) {
            info.textContent = 'Loading...';
        }
    }

    window.handleMediaCanPlay = function(mediaElement) {
        const container = mediaElement.closest('.media-section');
        const info = container.querySelector('.media-info span');
        if (info) {
            const duration = mediaElement.duration;
            if (duration && !isNaN(duration)) {
                const minutes = Math.floor(duration / 60);
                const seconds = Math.floor(duration % 60);
                const mediaType = mediaElement.tagName.toLowerCase();
                info.textContent = `${mediaType === 'video' ? 'Video' : 'Audio'} ready (${minutes}:${seconds.toString().padStart(2, '0')})`;
            } else {
                info.textContent = `${mediaElement.tagName.toLowerCase() === 'video' ? 'Video' : 'Audio'} ready`;
            }
        }
        announceToScreenReader('Media loaded and ready to play');
    }

    window.handleMediaError = function(mediaElement) {
        const container = mediaElement.closest('.media-section');
        const content = container.querySelector('.media-content');
        if (content) {
            const mediaType = mediaElement.tagName.toLowerCase();
            content.innerHTML = `
                <div class="media-error">
                    <p>Unable to load ${mediaType}. The file may not be available yet.</p>
                    <p><em>Please add the ${mediaType} file to the media folder.</em></p>
                </div>
            `;
        }
        announceToScreenReader('Media failed to load');
    }
    
    // Enhanced global function for back button in answer display
    window.goBackToCategoriesOrQuestions = function() {
        if (currentCategory !== null) {
            displayQuestions(currentCategory);
            announceToScreenReader('Returned to questions list');
        } else {
            displayCategories();
            announceToScreenReader('Returned to categories');
        }
    }

    function handleCopyCode(event) {
        const button = event.target.closest('.copy-code-btn');
        const codeContent = button.dataset.code || button.closest('.code-block').querySelector('pre').textContent;
        
        navigator.clipboard.writeText(codeContent).then(() => {
            button.innerHTML = '<span aria-hidden="true">✅</span> Copied!';
            button.style.background = 'var(--success-500)';
            button.style.color = 'white';
            announceToScreenReader('Code copied to clipboard');
            
            setTimeout(() => {
                button.innerHTML = '<span aria-hidden="true">📋</span> Copy';
                button.style.background = '';
                button.style.color = '';
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy code:', err);
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = codeContent;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            
            button.innerHTML = '<span aria-hidden="true">✅</span> Copied!';
            announceToScreenReader('Code copied to clipboard');
            setTimeout(() => {
                button.innerHTML = '<span aria-hidden="true">📋</span> Copy';
            }, 2000);
        });
    }

    function showTypingIndicator() {
        typingIndicator.style.display = 'block';
        typingIndicator.setAttribute('aria-hidden', 'false');
        announceToScreenReader('Sona is typing...');
        scrollToBottom();
    }

    function hideTypingIndicator() {
        typingIndicator.style.display = 'none';
        typingIndicator.setAttribute('aria-hidden', 'true');
    }

    function scrollToBottom() {
        requestAnimationFrame(() => {
            mainContentArea.scrollTop = mainContentArea.scrollHeight;
        });
    }

    function scrollToTop() {
        requestAnimationFrame(() => {
            mainContentArea.scrollTop = 0;
        });
    }

    // Enhanced error handling
    window.addEventListener('error', (event) => {
        console.error('Global error:', event.error);
        announceToScreenReader('An unexpected error occurred');
    });

    window.addEventListener('unhandledrejection', (event) => {
        console.error('Unhandled promise rejection:', event.reason);
        announceToScreenReader('An unexpected error occurred');
    });

    // Enhanced performance monitoring
    if ('performance' in window) {
        window.addEventListener('load', () => {
            const loadTime = performance.now();
            console.log(`Page loaded in ${loadTime.toFixed(2)}ms`);
        });
    }

    // --- Initialize ---
    displayCategories();
    console.log('Viraa Care Categorical Assistant initialized with enhanced accessibility and UX features.');
});