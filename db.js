import mysql from "mysql2/promise";
import dotenv from "dotenv";
dotenv.config();

const pool = mysql.createPool({
  uri: process.env.MYSQL_URL,
});

// Testing connection once at startup

async function testConn() {
  try {
    console.log("Establishing MySQL connection...");
    const conn = await pool.getConnection();
    console.log("MySQL connected successfully");
    conn.release();
  } catch (error) {
    console.log("MySQL connection failed", error.message);
    process.exit(1);
  }
}

await testConn();

export default pool;
