import { Box, Select } from 'dracula-ui';
import LabelCard from './LabelCard';
import './BookingView.css';

function BookingView() {
  return (
    <Box className="BookingView">
      <Box className="row">
        <LabelCard label="출발">
          <Select>
            <option value="default" disabled={true}>
              역을 선택해주세요
            </option>
            <option>서울</option>
            <option>동대구</option>
            <option>부산</option>
          </Select>
        </LabelCard>
        <LabelCard label="도착">
          <Select>
            <option value="default" disabled={true}>
              역을 선택해주세요
            </option>
            <option>서울</option>
            <option>동대구</option>
            <option>부산</option>
          </Select>
        </LabelCard>
      </Box>
    </Box>
  );
}

export default BookingView;
