import { Box, Text } from 'dracula-ui';
import { WaitingCard, Spinner } from 'components';
import { useQuery } from 'react-query';
import './WaitingView.css';

function WaitingView() {
  const { isLoading, error, data: tickets } = useQuery(
    'tickets',
    () => fetch(process.env.REACT_APP_API_HOST + '/tickets').then(res =>
      res.json()
    ),
    {
      retry: 1,
      refetchInterval: 1000,
    },
  );
  if (isLoading) {
    return (
      <Box className="WaitingView">
        <Spinner />
      </Box>
    );
  } else if (error || tickets.status !== 'success') {
    return (
      <Box className="WaitingView">
        <Text>An error has occurred.</Text>
      </Box>
    );
  } else {
    return (
      <Box className="WaitingView">
      {
        tickets.data.sort((a, b) => b.id - a.id).map((ticket) =>
          <WaitingCard
            key={ticket.id}
            departure_station={ticket.departure_station}
            arrival_station={ticket.arrival_station}
            date={ticket.date}
            departure_base={ticket.departure_base}
            arrival_limit={ticket.arrival_limit}
            reserved={ticket.reserved}
            running={ticket.running}
          />
        )
      }
      </Box>
    );
  }
}

export default WaitingView;
