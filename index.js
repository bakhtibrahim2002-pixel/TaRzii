import { voiceClient } from "./client.js";
import tokens from "./tokens.js";
import express from 'express';
const app = express();
const port = 3000;
let url = "";
let uptimeDate = Date.now();
let requests = 0;
let response = null;
app.use((req, res, next) => {
    const hostname = req.hostname;
    const subdomain = hostname.split('.')[0];
    const domain = hostname.replace(`${subdomain}.`, '');
    req.subdomain = subdomain;
    req.domain = domain;
    url = `https://${subdomain}.${domain}/`;
    next();
});
app.get('/', (req, res) => res.send('Hello World!'));
app.listen(port, () => console.log(`Example app listening at ${url}`));
process.on('uncaughtException', (err) => {
    console.error(`Uncaught Exception: ${err.message}`);
});
process.on('unhandledRejection', (reason, promise) => {
    console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});
setInterval(async () => {
    console.log(url);
    try {
        response = await fetch(url, { method: 'HEAD' });
        requests += 1;
        console.log(`Request done with status ${response.status} ${requests}`);
    } catch (error) {
        if (error.response) {
            requests += 1;
            console.log(`Response status: ${error.response.status}${requests}`);
        }
    } finally {
        response = null;
    }
}, 15000);
const cleanTokens = tokens.reduce((acc, token) => {
    const isValid = token?.token?.length > 30;
    const isDuplicate = acc.some(t => t.token === token.token);
    if (isValid && !isDuplicate) {
        acc.push(token);
    }
    else {
        console.warn('Invalid or duplicate token configuration:', token);
    }
    return acc;
}, []);
for (const token of cleanTokens) {
    const client = new voiceClient(token);
    client.on('ready', (user) => {
        console.log(`Logged in as ${user.username}#${user.discriminator}`);
    });
    client.on('connected', () => {
        console.log('Connected to Discord');
    });
    client.on('disconnected', () => {
        console.log('Disconnected from Discord');
    });
    client.on('voiceReady', () => {
        console.log('Voice is ready');
    });
    client.on('error', (error) => {
        console.error('Error:', error);
    });
    client.on('debug', (message) => {
        console.debug(message);
    });
    client.connect();
}
client.on('messageCreate', async message => {
    // تجاهل رسائل البوتات لكي لا يحدث تكرار لا نهائي
    if (message.author.bot) return;

    // مثال لأمر المسح: !clear والعدد بجانبه
    if (message.content.startsWith('!clear')) {
        // التحقق من صلاحيات المستخدم في السيرفر (مثلاً هل يملك صلاحية إدارة الرسائل)
        if (!message.member.permissions.has('ManageMessages')) {
            return message.reply('ليس لديك صلاحية لاستخدام هذا الأمر!');
        }

        const args = message.content.split(' ');
        const count = parseInt(args[1]);

        if (isNaN(count) || count <= 0 || count > 100) {
            return message.reply('الرجاء تحديد عدد صحيح بين 1 و 100 للحذف.');
        }

        try {
            // حذف الرسائل
            await message.channel.bulkDelete(count + 1, true);
            const reply = await message.channel.send(`تم بنجاح مسح ${count} رسالة.`);
            setTimeout(() => reply.delete(), 4000); // حذف رسالة التأكيد بعد 4 ثوانٍ
        } catch (error) {
            console.error(error);
            message.replyحدث خطأ أثناء محاولة مسح الرسائل.');
        }
    }
});
client.on('messageCreate', async message => {
    if (message.author.bot) return;

    if (message.content.startsWith('!giverole')) {
        // التحقق من صلاحية المستخدم (إدارة الرتب)
        if (!message.member.permissions.has('ManageRoles')) {
            return message.reply('ليس لديك صلاحية لإدارة الرتب!');
        }

        // استخراج العضو المذكور والرتبة المذكورة في الرسالة
        const member = message.mentions.members.first();
        const role = message.mentions.roles.first();

        if (!member || !role) {
            return message.reply('الرجاء تحديد العضو والرتبة بشكل صحيح. مثال: `!giverole @User @Role`');
        }

        try {
            // إعطاء الرتبة للعضو
            await member.roles.add(role);
            message.reply(`تم بنجاح إعطاء الرتبة ${role.name} إلى العضو ${member.user.tag}`);
        } catch (error) {
            console.error(error);
            message.reply('فشل البوت في إعطاء الرتبة. تأكد من أن رتبة البوت أعلى من الرتبة المراد إعطاؤها وأنه يملك صلاحية Manage Roles.');
        }
    }
});
