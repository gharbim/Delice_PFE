// material-ui
import { styled } from '@material-ui/styles';

// Image
import backgroundImage from '../../../assets/images/backroung_delice.jpg';
import backgroundImageDark from '../../../assets/images/backroung_delice.jpg';

//-----------------------|| AUTHENTICATION 1 WRAPPER ||-----------------------//

const AuthWrapper1 = styled('div')(({ theme }) => ({
    backgroundImage: `url(${theme.palette.mode === 'dark' ? backgroundImageDark : backgroundImage})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat',
    minHeight: '65vh'
}));

export default AuthWrapper1;


