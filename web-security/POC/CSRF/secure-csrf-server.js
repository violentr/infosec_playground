/**
 * SECURE CSRF SERVER - Demonstrates CSRF protection
 * 
 * This server has authentication AND CSRF token protection,
 * preventing cross-site request forgery attacks.
 */

const express = require('express');
const cookieParser = require('cookie-parser');
const crypto = require('crypto');
const app = express();
const PORT = 3002;

// Middleware
app.use(cookieParser());
app.use(express.json());

// CORS - restrict to specific origins
const allowedOrigins = ['http://localhost:8080', 'http://localhost:3000'];
app.use((req, res, next) => {
    const origin = req.headers.origin;
    if (allowedOrigins.includes(origin)) {
        res.setHeader('Access-Control-Allow-Origin', origin);
        res.setHeader('Access-Control-Allow-Credentials', 'true');
    }
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-CSRF-Token');
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
        password: 'password123',
        balance: 10000.00,
        accountNumber: '1234567890'
    }
};

// Simulated session store
const sessions = {};

// Helper function to generate CSRF token
function generateCSRFToken() {
    return crypto.randomBytes(32).toString('hex');
}

// Helper function to validate CSRF token
function validateCSRFToken(req, sessionId) {
    const session = sessions[sessionId];
    if (!session) {
        return false;
    }
    
    const tokenFromHeader = req.headers['x-csrf-token'];
    const tokenFromSession = session.csrfToken;
    
    if (!tokenFromHeader || !tokenFromSession) {
        return false;
    }
    
    // Use constant-time comparison to prevent timing attacks
    return crypto.timingSafeEqual(
        Buffer.from(tokenFromHeader),
        Buffer.from(tokenFromSession)
    );
}

// Login endpoint - generates CSRF token
app.post('/api/login', (req, res) => {
    const { username, password } = req.body;
    
    if (username === 'user123' && password === 'password123') {
        const sessionId = 'session_' + Date.now();
        const csrfToken = generateCSRFToken();
        
        // Store session with CSRF token
        sessions[sessionId] = { 
            userId: 'user123', 
            createdAt: Date.now(),
            csrfToken: csrfToken
        };
        
        // ✅ SECURE: SameSite=Strict prevents cross-site cookie sending
        res.cookie('sessionId', sessionId, {
            httpOnly: true,
            secure: false, // Set to true in production with HTTPS
            sameSite: 'strict', // ✅ Blocks cross-site requests
            maxAge: 24 * 60 * 60 * 1000
        });
        
        // Return CSRF token in response (client stores it)
        return res.json({ 
            success: true, 
            message: 'Logged in successfully',
            csrfToken: csrfToken, // ✅ Client must include this in requests
            user: {
                id: users[username].id,
                name: users[username].name,
                email: users[username].email
            }
        });
    }
    
    res.status(401).json({ error: 'Invalid credentials' });
});

// ✅ SECURE: CSRF token validation middleware
function requireCSRFToken(req, res, next) {
    const sessionId = req.cookies.sessionId;
    
    if (!sessionId || !sessions[sessionId]) {
        return res.status(401).json({ error: 'Unauthorized' });
    }
    
    // Validate CSRF token
    if (!validateCSRFToken(req, sessionId)) {
        console.log(`🛡️ CSRF ATTACK BLOCKED: Invalid or missing CSRF token`);
        return res.status(403).json({ 
            error: 'Invalid CSRF token',
            message: 'This request was blocked due to missing or invalid CSRF token'
        });
    }
    
    next();
}

// ✅ SECURE: Protected with CSRF token
app.post('/api/transfer', requireCSRFToken, (req, res) => {
    const sessionId = req.cookies.sessionId;
    const userId = sessions[sessionId].userId;
    const user = users[userId];
    
    const { to, amount } = req.body;
    
    if (!to || !amount) {
        return res.status(400).json({ error: 'Missing required fields: to, amount' });
    }
    
    if (amount > user.balance) {
        return res.status(400).json({ error: 'Insufficient funds' });
    }
    
    // ✅ CSRF token validated, safe to proceed
    user.balance -= amount;
    
    console.log(`✅ SECURE: Transferred $${amount} from ${user.id} to ${to}`);
    
    res.json({
        success: true,
        message: 'Transfer completed',
        from: user.accountNumber,
        to: to,
        amount: amount,
        newBalance: user.balance
    });
});

// ✅ SECURE: Protected with CSRF token
app.post('/api/change-password', requireCSRFToken, (req, res) => {
    const sessionId = req.cookies.sessionId;
    const userId = sessions[sessionId].userId;
    const user = users[userId];
    
    const { newPassword, confirmPassword } = req.body;
    
    if (!newPassword || newPassword !== confirmPassword) {
        return res.status(400).json({ error: 'Passwords do not match' });
    }
    
    // ✅ CSRF token validated, safe to proceed
    user.password = newPassword;
    
    console.log(`✅ SECURE: Password changed for ${user.id}`);
    
    res.json({
        success: true,
        message: 'Password changed successfully'
    });
});

// ✅ SECURE: Protected with CSRF token
app.post('/api/change-email', requireCSRFToken, (req, res) => {
    const sessionId = req.cookies.sessionId;
    const userId = sessions[sessionId].userId;
    const user = users[userId];
    
    const { newEmail } = req.body;
    
    if (!newEmail) {
        return res.status(400).json({ error: 'Email is required' });
    }
    
    // ✅ CSRF token validated, safe to proceed
    user.email = newEmail;
    
    console.log(`✅ SECURE: Email changed for ${user.id} to ${newEmail}`);
    
    res.json({
        success: true,
        message: 'Email changed successfully',
        newEmail: newEmail
    });
});

// Get account balance (read-only, no CSRF needed)
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
    res.json({ status: 'ok', server: 'secure-csrf' });
});

app.listen(PORT, () => {
    console.log(`\n✅ SECURE CSRF SERVER running on http://localhost:${PORT}`);
    console.log(`\n🛡️  This server has CSRF protection enabled.`);
    console.log(`\n📝 Test credentials:`);
    console.log(`   Username: user123`);
    console.log(`   Password: password123`);
    console.log(`\n🔗 Endpoints:`);
    console.log(`   POST http://localhost:${PORT}/api/login`);
    console.log(`   POST http://localhost:${PORT}/api/transfer (🛡️ PROTECTED)`);
    console.log(`   POST http://localhost:${PORT}/api/change-password (🛡️ PROTECTED)`);
    console.log(`   POST http://localhost:${PORT}/api/change-email (🛡️ PROTECTED)`);
    console.log(`   GET  http://localhost:${PORT}/api/account-balance`);
    console.log(`\n💡 Protection methods:`);
    console.log(`   ✅ CSRF tokens required for state-changing operations`);
    console.log(`   ✅ SameSite=Strict cookies`);
    console.log(`   ✅ Origin validation`);
    console.log(`\n`);
});

