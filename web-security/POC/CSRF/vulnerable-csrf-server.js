/**
 * VULNERABLE CSRF SERVER - Demonstrates CSRF vulnerability
 * 
 * This server has authentication but NO CSRF protection,
 * making it vulnerable to cross-site request forgery attacks.
 */

const express = require('express');
const cookieParser = require('cookie-parser');
const cors = require('cors');
const app = express();
const PORT = 3001;

// Middleware
app.use(cookieParser());
app.use(express.json());

// ⚠️ VULNERABLE: Allows all origins and credentials
app.use((req, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', req.headers.origin || '*');
    res.setHeader('Access-Control-Allow-Credentials', 'true');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    if (req.method === 'OPTIONS') {
        return res.status(204).end();
    }
    next();
});

// Simulated user database
const users = {
    'user123': {
        id: 'user123',
        name: 'John Doe',
        email: 'john@example.com',
        password: 'password123', // In real app, this would be hashed
        balance: 10000.00,
        accountNumber: '1234567890'
    }
};

// Simulated session store
const sessions = {};

// Login endpoint
app.post('/api/login', (req, res) => {
    const { username, password } = req.body;
    
    if (username === 'user123' && password === 'password123') {
        const sessionId = 'session_' + Date.now();
        sessions[sessionId] = { userId: 'user123', createdAt: Date.now() };
        
        // ⚠️ VULNERABLE: SameSite=Lax allows some cross-site requests
        res.cookie('sessionId', sessionId, {
            httpOnly: true,
            secure: false, // Should be true in production with HTTPS
            sameSite: 'lax', // ⚠️ Allows cookies on GET requests from other sites
            maxAge: 24 * 60 * 60 * 1000 // 24 hours
        });
        
        return res.json({ 
            success: true, 
            message: 'Logged in successfully',
            user: {
                id: users[username].id,
                name: users[username].name,
                email: users[username].email
            }
        });
    }
    
    res.status(401).json({ error: 'Invalid credentials' });
});

// ⚠️ VULNERABLE: No CSRF token validation
app.post('/api/transfer', (req, res) => {
    const sessionId = req.cookies.sessionId;
    
    if (!sessionId || !sessions[sessionId]) {
        return res.status(401).json({ error: 'Unauthorized - Please login' });
    }
    
    const userId = sessions[sessionId].userId;
    const user = users[userId];
    
    if (!user) {
        return res.status(404).json({ error: 'User not found' });
    }
    
    const { to, amount } = req.body;
    
    if (!to || !amount) {
        return res.status(400).json({ error: 'Missing required fields: to, amount' });
    }
    
    if (amount > user.balance) {
        return res.status(400).json({ error: 'Insufficient funds' });
    }
    
    // ⚠️ VULNERABLE: No CSRF token check!
    // In a real attack, this would transfer money to attacker's account
    user.balance -= amount;
    
    console.log(`⚠️ CSRF ATTACK: Transferred $${amount} from ${user.id} to ${to}`);
    
    res.json({
        success: true,
        message: 'Transfer completed',
        from: user.accountNumber,
        to: to,
        amount: amount,
        newBalance: user.balance
    });
});

// ⚠️ VULNERABLE: No CSRF token validation
app.post('/api/change-password', (req, res) => {
    const sessionId = req.cookies.sessionId;
    
    if (!sessionId || !sessions[sessionId]) {
        return res.status(401).json({ error: 'Unauthorized' });
    }
    
    const userId = sessions[sessionId].userId;
    const user = users[userId];
    
    const { newPassword, confirmPassword } = req.body;
    
    if (!newPassword || newPassword !== confirmPassword) {
        return res.status(400).json({ error: 'Passwords do not match' });
    }
    
    // ⚠️ VULNERABLE: No CSRF token check!
    user.password = newPassword; // In real app, hash this
    
    console.log(`⚠️ CSRF ATTACK: Password changed for ${user.id}`);
    
    res.json({
        success: true,
        message: 'Password changed successfully',
        newPassword: newPassword // ⚠️ Don't do this in production!
    });
});

// ⚠️ VULNERABLE: No CSRF token validation
app.post('/api/change-email', (req, res) => {
    const sessionId = req.cookies.sessionId;
    
    if (!sessionId || !sessions[sessionId]) {
        return res.status(401).json({ error: 'Unauthorized' });
    }
    
    const userId = sessions[sessionId].userId;
    const user = users[userId];
    
    const { newEmail } = req.body;
    
    if (!newEmail) {
        return res.status(400).json({ error: 'Email is required' });
    }
    
    // ⚠️ VULNERABLE: No CSRF token check!
    user.email = newEmail;
    
    console.log(`⚠️ CSRF ATTACK: Email changed for ${user.id} to ${newEmail}`);
    
    res.json({
        success: true,
        message: 'Email changed successfully',
        newEmail: newEmail
    });
});

// Get account balance
app.get('/api/account-balance', (req, res) => {
    const sessionId = req.cookies.sessionId;
    
    if (!sessionId || !sessions[sessionId]) {
        return res.status(401).json({ error: 'Unauthorized' });
    }
    
    const userId = sessions[sessionId].userId;
    const user = users[userId];
    
    res.json({
        balance: user.balance,
        accountNumber: user.accountNumber,
        currency: 'USD'
    });
});

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'ok', server: 'vulnerable-csrf' });
});

app.listen(PORT, () => {
    console.log(`\n🚨 VULNERABLE CSRF SERVER running on http://localhost:${PORT}`);
    console.log(`\n⚠️  This server is intentionally vulnerable for CSRF demonstration.`);
    console.log(`\n📝 Test credentials:`);
    console.log(`   Username: user123`);
    console.log(`   Password: password123`);
    console.log(`\n🔗 Endpoints:`);
    console.log(`   POST http://localhost:${PORT}/api/login`);
    console.log(`   POST http://localhost:${PORT}/api/transfer (⚠️ VULNERABLE)`);
    console.log(`   POST http://localhost:${PORT}/api/change-password (⚠️ VULNERABLE)`);
    console.log(`   POST http://localhost:${PORT}/api/change-email (⚠️ VULNERABLE)`);
    console.log(`   GET  http://localhost:${PORT}/api/account-balance`);
    console.log(`\n💡 To test CSRF:`);
    console.log(`   1. Login at http://localhost:${PORT}/api/login`);
    console.log(`   2. Open csrf-demo.html in browser`);
    console.log(`   3. Click attack buttons to see CSRF in action`);
    console.log(`\n`);
});

