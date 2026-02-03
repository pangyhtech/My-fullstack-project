/**
 * MonotaRO Q&A System - Frontend Logic
 * Handles category/product selection and chat interaction
 */

const API_BASE = '';

// DOM Elements
const categorySelect = document.getElementById('category-select');
const productSelect = document.getElementById('product-select');
const productInfoPanel = document.getElementById('product-info-panel');
const infoName = document.getElementById('info-name');
const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const loading = document.getElementById('loading');
const resetBtn = document.getElementById('reset-btn');

let currentCategoryName = '';
let currentProductName = '';

// Icons for satisfaction
const SATISFACTION_ICONS = {
    0: '😞', // Dissatisfied
    1: '😐', // Neutral
    2: '😊'  // Satisfied
};

/**
 * Initialize
 */
async function init() {
    await loadCategories();

    // Event Listeners
    categorySelect.addEventListener('change', handleCategoryChange);
    productSelect.addEventListener('change', handleProductChange);
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
    resetBtn.addEventListener('click', resetDialogue);
}

/**
 * Load Categories
 */
async function loadCategories() {
    try {
        const res = await fetch(`${API_BASE}/api/categories`);
        const data = await res.json();

        categorySelect.innerHTML = '<option value="" disabled selected>カテゴリを選択...</option>';
        productSelect.innerHTML = '<option value="" disabled selected>先にカテゴリを選択...</option>';
        productSelect.disabled = true;

        data.categories.forEach((cat, index) => {
            const option = document.createElement('option');
            option.value = index; // Use index as ID
            option.textContent = cat.name;
            categorySelect.appendChild(option);
        });
    } catch (e) {
        console.error("Failed to load categories:", e);
        showError("カテゴリの読み込みに失敗しました");
    }
}

/**
 * Handle Category Change
 */
async function handleCategoryChange(e) {
    const categoryId = e.target.value;
    const selectedOption = e.target.options[e.target.selectedIndex];
    currentCategoryName = selectedOption.textContent;

    // Reset Product Select
    productSelect.innerHTML = '<option value="" disabled selected>読み込み中...</option>';
    productSelect.disabled = true;
    hideProductInfo();

    try {
        // Notify Backend
        await fetch(`${API_BASE}/api/select_category`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ category_id: parseInt(categoryId) })
        });

        // Fetch Products for this Category
        const res = await fetch(`${API_BASE}/api/products/${categoryId}`);
        const data = await res.json();

        productSelect.innerHTML = '<option value="" disabled selected>商品を選択...</option>';
        data.products.forEach(prod => {
            const option = document.createElement('option');
            option.value = prod;
            option.textContent = prod;
            productSelect.appendChild(option);
        });
        productSelect.disabled = false;

    } catch (e) {
        console.error("Error selecting category:", e);
        showError("カテゴリ選択時にエラーが発生しました");
    }
}

/**
 * Handle Product Change
 */
async function handleProductChange(e) {
    const productName = e.target.value;
    currentProductName = productName;

    try {
        const res = await fetch(`${API_BASE}/api/select_product`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ product_name: productName })
        });
        const data = await res.json();

        if (data.success) {
            showProductInfo(productName, data.price);
            enableChat();
            addSystemMessage(`「${productName}」が選択されました。ご質問をどうぞ。`);
        } else {
            showError(data.error);
        }

    } catch (e) {
        console.error("Error selecting product:", e);
        showError("商品選択時にエラーが発生しました");
    }
}

/**
 * Send Message
 */
async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    addMessage(text, 'user');
    userInput.value = '';
    showLoading(true);

    try {
        const res = await fetch(`${API_BASE}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        const data = await res.json();

        showLoading(false);
        addMessage(data.response, 'bot', data);

    } catch (e) {
        showLoading(false);
        addMessage("申し訳ございません。通信エラーが発生しました。", 'bot');
    }
}

/**
 * Reset
 */
async function resetDialogue() {
    await fetch(`${API_BASE}/api/reset`, { method: 'POST' });

    // Clear Chat
    chatBox.innerHTML = `
        <div class="message system">
            <div class="bubble">
                <p>会話がリセットされました。<br>新たにお問い合わせください。</p>
            </div>
        </div>
    `;

    // Reset Selections
    categorySelect.value = "";
    productSelect.innerHTML = '<option value="" disabled selected>先にカテゴリを選択...</option>';
    productSelect.disabled = true;
    hideProductInfo();
    disableChat();
}

/**
 * UI Helpers
 */
function showProductInfo(name, price) {
    productInfoPanel.style.display = 'block';
    infoName.textContent = name;
    // Price could be added here if we had a price element
}

function hideProductInfo() {
    productInfoPanel.style.display = 'none';
    infoName.textContent = '-';
}

function enableChat() {
    userInput.disabled = false;
    sendBtn.disabled = false;
    userInput.placeholder = "質問を入力してください...";
    userInput.focus();
}

function disableChat() {
    userInput.disabled = true;
    sendBtn.disabled = true;
    userInput.placeholder = "左側のメニューから商品を選択してください";
}

function showLoading(show) {
    loading.style.display = show ? 'flex' : 'none';
}

function addMessage(text, type, meta = null) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${type}`;

    let avatarHtml = type === 'user'
        ? '<div class="avatar" style="background:#cc0000; color:white; display:flex; align-items:center; justify-content:center; border-radius:50%; width:32px; height:32px;"><i class="fas fa-user"></i></div>'
        : '<div class="avatar operator-avatar" style="background:#888888; color:white; display:flex; align-items:center; justify-content:center; border-radius:50%; width:32px; height:32px;"><i class="fas fa-headset"></i></div>';

    let metaHtml = '';
    if (meta && type === 'bot') {
        const satLabel = meta.satisfaction_label || 'Neutral';
        const satClass = meta.satisfaction === 2 ? 'positive' : (meta.satisfaction === 0 ? 'negative' : 'neutral');
        metaHtml = `
            <div class="satisfaction-tag ${satClass}">
                <span class="sat-prefix">顧客満足度予測:</span> ${satLabel}
            </div>
        `;
    }

    msgDiv.innerHTML = `
        ${type === 'bot' ? avatarHtml : ''}
        <div class="bubble">
            ${escapeHtml(text)}
            ${metaHtml}
        </div>
        ${type === 'user' ? avatarHtml : ''}
    `;

    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function addSystemMessage(text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message system';
    msgDiv.innerHTML = `<div class="bubble"><p>${text}</p></div>`;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function showError(msg) {
    alert(msg);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML.replace(/\n/g, '<br>');
}

// Start
init();
