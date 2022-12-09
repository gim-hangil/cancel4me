import { Box } from 'dracula-ui';
import { WaitingCard } from 'components';
import './WaitingView.css';

function WaitingView() {
  return (
    <Box className="WaitingView">
      <WaitingCard done={true} />
      <WaitingCard done={false} />
      <WaitingCard done={false} />
    </Box>
  );
}

export default WaitingView;
