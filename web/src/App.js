import { Box, Heading, Tabs, Text } from 'dracula-ui';
import { useState } from 'react';
import BookingView from './BookingView';
import './App.css';

function App() {
  const [tab, setTab] = useState('book');
  return (
    <Box className="App" width="full" mx="auto" my="xs">
      <Box className="heading" my="sm">
        <Heading>
          취소표가 필요해!
        </Heading>
      </Box>
      <Tabs className="tabs">
        <li
          className={[
            'drac-tab',
            tab === 'book' ? 'drac-tab-active' : ''
          ].join(' ')}
          onClick={() => setTab('book')}
        >
          <Text>예매</Text>
        </li>
        <li
          className={[
            'drac-tab',
            tab === 'list' ? 'drac-tab-active' : ''
          ].join(' ')}
          onClick={() => setTab('list')}
        >
          <Text>대기 중</Text>
        </li>
      </Tabs>
      {
        tab === 'book' ?
        <BookingView /> :
        <Box></Box>
      }
    </Box>
  );
}

export default App;
