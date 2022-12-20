import { Box } from 'dracula-ui';
import { WaitingCard } from 'components';
import { useEffect, useState } from 'react';
import './WaitingView.css';

function WaitingView() {
  const [ tickets, setTickets ] = useState([]);
  useEffect(() => {
    const cached = window.sessionStorage.getItem('tickets');
    if (cached !== null) {
      setTickets(JSON.parse(cached));
      return;
    }
    (async () => {
      const res = await fetch(process.env.REACT_APP_API_HOST + '/tickets');
      const json = await res.json();
      if (json.status === 'success') {
        setTickets(json.data.sort((a, b) => b.id - a.id));
        window.sessionStorage.setItem('tickets', JSON.stringify(json.data));
      }
    })();
  }, []);
  return (
    <Box className="WaitingView">
      {
        tickets.map((ticket) =>
          <WaitingCard
            key={ticket.id}
            departure_station={ticket.departure_station}
            arrival_station={ticket.arrival_station}
            date={ticket.date}
            departure_base={ticket.departure_base}
            arrival_limit={ticket.arrival_limit}
            reserved={ticket.reserved}
          />
        )
      }
    </Box>
  );
}

export default WaitingView;
