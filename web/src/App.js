import { Anchor, Paragraph } from 'dracula-ui';
import 'dracula-ui/styles/dracula-ui.css'
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Paragraph>
          Edit <code>src/App.js</code> and save to reload.
        </Paragraph>
        <Anchor
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </Anchor>
      </header>
    </div>
  );
}

export default App;
