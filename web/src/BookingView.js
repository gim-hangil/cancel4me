import { Box } from 'dracula-ui';
import SelectStation from './SelectStation';
import './BookingView.css';

function BookingView() {
  return (
    <Box className="BookingView">
      <Box className="row">
        <SelectStation label="출발" />
        <SelectStation label="도착" />
      </Box>
    </Box>
  );
}

export default BookingView;
