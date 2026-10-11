export const isSuperUser = (user) => Boolean(user?.is_superuser);

const SUPERUSER_ONLY_PATHS = ['/admin/users'];

export const canAccessPath = (user, pathname) => {
    if (SUPERUSER_ONLY_PATHS.includes(pathname)) {
        return isSuperUser(user);
    }
    return true;
};
