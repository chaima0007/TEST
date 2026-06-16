const createApp = require('./app');

const PORT = process.env.PORT || 4000;
const app = createApp();

app.listen(PORT, () => {
  console.log(`Moonbow SAS website running on http://localhost:${PORT}`);
});
