import { Box, Heading, Tabs, Text } from 'dracula-ui';
import { useState } from 'react';
import BookingView from './BookingView';
import WaitingView from './WaitingView';
import WelcomeView from './WelcomeView';
import './App.css';

function App() {
  const [tabNo, setTabNo] = useState(0);
  const tabs = [
    {
      label: '소개',
      viewComponent: <WelcomeView />,
    },
    {
      label: '예매',
      viewComponent: <BookingView />,
    },
    {
      label: '대기 중',
      viewComponent: <WaitingView />,
    },
  ];
  return (
    <Box className="App" width="full" mx="auto" my="xs">
      <Box className="heading" my="sm">
        <Heading>
          취소표가 필요해!
        </Heading>
      </Box>
      <Tabs className="tabs">
      {
        tabs.map((tabItem, index) =>
          <li
            key={[
              tabItem.label,
              tabNo === index ? 'active' : ''
            ].join(' ')}
            className={[
              'drac-tab',
              tabNo === index ? 'drac-tab-active' : ''
            ].join(' ')}
            onClick={() => setTabNo(index)}
          >
            <Text>{ tabItem.label }</Text>
          </li>
        )
      }
      </Tabs>
      { tabs[tabNo].viewComponent }
    </Box>
  );
}

export default App;
