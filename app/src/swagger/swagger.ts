import swaggerAutogen from "swagger-autogen";
import path from "path";
import dotenv from "dotenv";

dotenv.config();
const PORT = process.env.PORT || 3000;

const doc = {
    info: {
        title: "API Documentation",
        description: "API Documentation for the project",
    },
    servers: [
        {
            url: "http://" + process.env.SERVER_IP + ":" + PORT.toString()
        }
            
    ],
    schemes: ["http"],
    securityDefinitions: {
        bearerAuth: {
            type: "http",
            scheme: "bearer",
            in: "header",
            bearerFormat: "JWT",
        },
    },
    components: {
        '@schemas': {
            Coordinates: {
                type: "object",
                properties: {
                    lon: {
                        type: "number",
                        format: "double",
                        example: 127.109457691,
                    },
                    lat: {
                        type: "number",
                        format: "double",
                        example: 37.510190298,
                    },
                },
            },
            CurrentLocation: {
                type: "object",
                properties: {
                    coordinates: {
                        $ref: "#/components/schemas/Coordinates",
                    },
                    distance: {
                        type: "number",
                        format: "double",
                        example: 5000,
                    }
                },
            },
            ClothBox: {
                type: "object",
                properties: {
                    _id: {
                        type: "string",
                        example: "6679527999198cb22dccbb34",
                    },
                    address: {
                        type: "string",
                        example: "송파동 22-6",
                    },
                    coordinates: {
                        $ref: "#/components/schemas/Coordinates",
                    },
                },
            },
        }
    },
};

const outputFile = path.join(__dirname, "swagger-output.json");
const endpointsFiles = [path.join(__dirname, "../routes/**/*.ts")];

swaggerAutogen({openapi: '3.0.0'})(outputFile, endpointsFiles, doc);