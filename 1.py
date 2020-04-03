def main():
    global_init(input())
    session = create_session()
    # u = []
    for user in session.query(User).all():
        for job in session.query(Jobs).filter((Jobs.collaborators.like(f'%{user.id}%') | (Jobs.team_leader == user.id)),
                                              Jobs.work_size >= 25):
            for d in session.query(Department).filter(Department.id == 1,
                                                      (Department.members.like(f'%{user.id}%') |
                                                       (Department.chief == user.id))):
                print(f'{user.surname} {user.name}')
                break
            break
    #             if f'{user.surname} {user.name}' not in u:
    #                 u.append()
    # for i in u:
    #     print(i)


if __name__ == '__main__':
    main()
