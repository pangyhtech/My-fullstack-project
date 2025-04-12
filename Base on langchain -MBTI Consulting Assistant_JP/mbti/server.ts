import express from 'express';
import cors from 'cors';
import { getMBTIChatChain, mbtiInfo, mbtiList } from './index.ts';

const app = express();
app.use(cors());
app.use(express.json());

const mbtiChain = await getMBTIChatChain();

app.post('/chat', async (req, res) => {
    try {
        const { type, question } = req.body;
        const info = mbtiInfo[type.toLowerCase()];
        
        const response = await mbtiChain.invoke({ type, question, info });
        res.json({ response });
    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ error: '服务器错误' });
    }
});

app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});