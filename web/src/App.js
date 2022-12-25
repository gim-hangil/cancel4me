import { Box, Heading, Tabs, Text } from 'dracula-ui';
import { useState } from 'react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { BookingView, WaitingView, WelcomeView } from 'views';
import './App.css';

const queryClient = new QueryClient();

function App() {
  const [tabNo, setTabNo] = useState(0);
  const tabs = [
    {
      label: '소개',
      viewComponent: <WelcomeView />,
    },
    {
      label: '예매',
      viewComponent: <BookingView onSuccess={() => setTabNo(2)} />,
    },
    {
      label: '대기 중',
      viewComponent: <WaitingView />,
    },
  ];
  return (
    <QueryClientProvider client={queryClient}>
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
    </QueryClientProvider>
  );
}

export default App;
