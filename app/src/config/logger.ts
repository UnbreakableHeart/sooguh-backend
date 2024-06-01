import { createLogger, transports, format } from "winston";

class Logger{
    private static instance: Logger;
    private logger: any;

    private printFormat = format.printf(({ timestamp, level, message }) => 
    {
        return `${timestamp} [${level}]: ${message}`;
    });

    private printLogFomat: any = {
        file: format.combine(
            //format.colorize()
            format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
            this.printFormat
        ),
        console: format.combine(
            format.colorize(),
            format.simple()
        )
    };

    private options: any = {
        file: new transports.File({
            filename: 'app.log',
            dirname: './logs',
            level: 'info',
            format: this.printLogFomat.file
        }),
        console: new transports.Console({
            level: 'debug',
            format: this.printLogFomat.console
        })
    };

    private constructor() {
        this.logger = createLogger({
            transports: [
                this.options.file,
            ]
        });
        if (process.env.NODE_ENV!== 'production') {
            this.logger.add(this.options.console);
        }
    };

    public static getInstance(): Logger {
        if (!this.instance) {
            this.instance = new Logger();
        }
        return this.instance;
    };

    public info(message: string) {
        this.logger.info(message);
    };

    public debug(message: string) {
        this.logger.debug(message);
    };

    public error(message: string) {
        this.logger.error(message);
    };
}

export default Logger;