import cors from 'cors';

// 허용 url
const whitelist = ["http://localhost:3000"];

// 옵션
const corsOptions : cors.CorsOptions = {
    origin: whitelist,
    credentials: true,
    optionsSuccessStatus: 200
}

export default corsOptions;