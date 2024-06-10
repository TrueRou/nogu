/**
 * This file was auto-generated by openapi-typescript.
 * Do not make direct changes to the file.
 */


export interface paths {
  "/": {
    /** Root */
    get: operations["root__get"];
  };
  "/users/me": {
    /** Users:Current User */
    get: operations["users_current_user_users_me_get"];
    /** Users:Patch Current User */
    patch: operations["users_patch_current_user_users_me_patch"];
  };
  "/users/{id}": {
    /** Users:User */
    get: operations["users_user_users__id__get"];
    /** Users:Delete User */
    delete: operations["users_delete_user_users__id__delete"];
    /** Users:Patch User */
    patch: operations["users_patch_user_users__id__patch"];
  };
  "/auth/jwt/login": {
    /** Auth:Jwt.Login */
    post: operations["auth_jwt_login_auth_jwt_login_post"];
  };
  "/auth/jwt/logout": {
    /** Auth:Jwt.Logout */
    post: operations["auth_jwt_logout_auth_jwt_logout_post"];
  };
  "/auth/register": {
    /** Register:Register */
    post: operations["register_register_auth_register_post"];
  };
  "/scores/{score_id}": {
    /** Get Score */
    get: operations["get_score_scores__score_id__get"];
  };
  "/scores/": {
    /** Submit Score */
    post: operations["submit_score_scores__post"];
  };
  "/scores/partial/": {
    /** Submit Score Partial */
    post: operations["submit_score_partial_scores_partial__post"];
  };
  "/scores/inspect/bancho/{match_id}": {
    /** Inspect Bancho Match */
    post: operations["inspect_bancho_match_scores_inspect_bancho__match_id__post"];
  };
  "/beatmaps/{ident}": {
    /** Get Beatmap */
    get: operations["get_beatmap_beatmaps__ident__get"];
  };
  "/beatmaps/stream/": {
    /** Stream Beatmap */
    post: operations["stream_beatmap_beatmaps_stream__post"];
  };
  "/teams/": {
    /** Get Teams */
    get: operations["get_teams_teams__get"];
  };
  "/teams/{team_id}": {
    /** Get Team */
    get: operations["get_team_teams__team_id__get"];
    /** Create Team */
    post: operations["create_team_teams__team_id__post"];
    /** Patch Team */
    patch: operations["patch_team_teams__team_id__patch"];
  };
  "/teams/me/": {
    /** Get Teams Me */
    get: operations["get_teams_me_teams_me__get"];
  };
  "/teams/scores/": {
    /** Get Scores */
    get: operations["get_scores_teams_scores__get"];
  };
  "/teams/stages/": {
    /** Get Stages */
    get: operations["get_stages_teams_stages__get"];
  };
  "/stages/{stage_id}": {
    /** Get Stage */
    get: operations["get_stage_stages__stage_id__get"];
    /** Patch Stage */
    patch: operations["patch_stage_stages__stage_id__patch"];
  };
  "/stages/": {
    /** Create Stage */
    post: operations["create_stage_stages__post"];
  };
  "/stages/beatmaps/": {
    /** Get Stage Beatmaps */
    get: operations["get_stage_beatmaps_stages_beatmaps__get"];
    /** Add Stage Beatmaps */
    post: operations["add_stage_beatmaps_stages_beatmaps__post"];
  };
  "/oauth/bancho/token": {
    /** Process Bancho Oauth */
    get: operations["process_bancho_oauth_oauth_bancho_token_get"];
  };
}

export type webhooks = Record<string, never>;

export interface components {
  schemas: {
    /** BearerResponse */
    BearerResponse: {
      /** Access Token */
      access_token: string;
      /** Token Type */
      token_type: string;
    };
    /** Beatmap */
    Beatmap: {
      /** Md5 */
      md5: string;
      /** Id */
      id: number | null;
      /** Set Id */
      set_id: number | null;
      /** Ranked Status */
      ranked_status: number;
      /** Artist */
      artist: string;
      /** Title */
      title: string;
      /** Version */
      version: string;
      /** Creator */
      creator: string;
      /** Filename */
      filename: string;
      /** Total Length */
      total_length: number;
      /** Max Combo */
      max_combo: number;
      ruleset: components["schemas"]["Ruleset"];
      /** Bpm */
      bpm: number;
      /** Cs */
      cs: number;
      /** Ar */
      ar: number;
      /** Od */
      od: number;
      /** Hp */
      hp: number;
      /** Star Rating */
      star_rating: number;
      /**
       * Osu Server
       * @default 2
       */
      osu_server?: number;
      /**
       * Server Updated At
       * Format: date-time
       */
      server_updated_at: string;
      /**
       * Created At
       * Format: date-time
       */
      created_at?: string;
      /**
       * Checked At
       * Format: date-time
       */
      checked_at?: string;
      /** Uploaded By */
      uploaded_by?: number | null;
    };
    /** Body_auth_jwt_login_auth_jwt_login_post */
    Body_auth_jwt_login_auth_jwt_login_post: {
      /** Grant Type */
      grant_type?: string | null;
      /** Username */
      username: string;
      /** Password */
      password: string;
      /**
       * Scope
       * @default
       */
      scope?: string;
      /** Client Id */
      client_id?: string | null;
      /** Client Secret */
      client_secret?: string | null;
    };
    /** ErrorModel */
    ErrorModel: {
      /** Detail */
      detail: string | {
        [key: string]: string;
      };
    };
    /** HTTPValidationError */
    HTTPValidationError: {
      /** Detail */
      detail?: components["schemas"]["ValidationError"][];
    };
    /**
     * Mods
     * @enum {integer}
     */
    Mods: 0 | 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 | 512 | 1024 | 2048 | 4096 | 8192 | 16384 | 32768 | 65536 | 131072 | 262144 | 524288 | 1048576 | 2097152 | 4194304 | 8388608 | 16777216 | 33554432 | 67108864 | 134217728 | 268435456 | 536870912 | 1073741824;
    /**
     * Ruleset
     * @enum {integer}
     */
    Ruleset: 0 | 1 | 2 | 3 | 4 | 5 | 6 | 8;
    /** Score */
    Score: {
      /** Score */
      score: number;
      /** Accuracy */
      accuracy: number;
      /** Highest Combo */
      highest_combo: number;
      mods: components["schemas"]["Mods"];
      /** Num 300S */
      num_300s: number;
      /** Num 100S */
      num_100s: number;
      /** Num 50S */
      num_50s: number;
      /** Num Misses */
      num_misses: number;
      /** Num Gekis */
      num_gekis: number;
      /** Num Katus */
      num_katus: number;
      ruleset: components["schemas"]["Ruleset"];
      /**
       * Osu Server
       * @default 2
       */
      osu_server?: number;
      /** Beatmap Md5 */
      beatmap_md5: string;
      /** Id */
      id?: number | null;
      /** Full Combo */
      full_combo: boolean;
      /** Grade */
      grade: string;
      /**
       * Created At
       * Format: date-time
       */
      created_at?: string;
      /** User Id */
      user_id: number;
      /** Stage Id */
      stage_id: number | null;
    };
    /** ScoreBase */
    ScoreBase: {
      /** Score */
      score: number;
      /** Accuracy */
      accuracy: number;
      /** Highest Combo */
      highest_combo: number;
      mods: components["schemas"]["Mods"];
      /** Num 300S */
      num_300s: number;
      /** Num 100S */
      num_100s: number;
      /** Num 50S */
      num_50s: number;
      /** Num Misses */
      num_misses: number;
      /** Num Gekis */
      num_gekis: number;
      /** Num Katus */
      num_katus: number;
      ruleset: components["schemas"]["Ruleset"];
      /**
       * Osu Server
       * @default 2
       */
      osu_server?: number;
      /** Beatmap Md5 */
      beatmap_md5: string;
    };
    /** Stage */
    Stage: {
      /** Name */
      name: string;
      /** Description */
      description: string | null;
      ruleset: components["schemas"]["Ruleset"];
      win_condition: components["schemas"]["WinCondition"];
      /** Playlist Id */
      playlist_id: number | null;
      /** Id */
      id?: number | null;
      /**
       * Version
       * @default 0
       */
      version?: number;
      /**
       * Created At
       * Format: date-time
       */
      created_at?: string;
      /**
       * Updated At
       * Format: date-time
       */
      updated_at?: string;
      /** Team Id */
      team_id: number;
    };
    /** StageBase */
    StageBase: {
      /** Name */
      name: string;
      /** Description */
      description: string | null;
      ruleset: components["schemas"]["Ruleset"];
      win_condition: components["schemas"]["WinCondition"];
      /** Playlist Id */
      playlist_id: number | null;
    };
    /** StageMapBase */
    StageMapBase: {
      /** Map Md5 */
      map_md5: string;
      /** Label */
      label: string;
      /** Description */
      description: string | null;
      represent_mods: components["schemas"]["Mods"];
      /** Condition Id */
      condition_id: number;
    };
    /** StageUpdate */
    StageUpdate: {
      /** Name */
      name: string | null;
      /** Description */
      description: string | null;
      win_condition: components["schemas"]["WinCondition"] | null;
    };
    /** Team */
    Team: {
      /** Name */
      name: string;
      /** Slogan */
      slogan: string | null;
      /** @default 2 */
      visibility?: components["schemas"]["TeamVisibility"];
      /** Active Until */
      active_until: string | null;
      /** Id */
      id?: number | null;
      /**
       * Active
       * @default true
       */
      active?: boolean;
      /**
       * Created At
       * Format: date-time
       */
      created_at?: string;
      /**
       * Updated At
       * Format: date-time
       */
      updated_at?: string;
    };
    /** TeamBase */
    TeamBase: {
      /** Name */
      name: string;
      /** Slogan */
      slogan: string | null;
      /** @default 2 */
      visibility?: components["schemas"]["TeamVisibility"];
      /** Active Until */
      active_until: string | null;
    };
    /**
     * TeamRole
     * @enum {integer}
     */
    TeamRole: 1 | 2 | 3;
    /** TeamUserLinkPublic */
    TeamUserLinkPublic: {
      role: components["schemas"]["TeamRole"];
      user: components["schemas"]["UserRead"];
    };
    /**
     * TeamVisibility
     * @enum {integer}
     */
    TeamVisibility: 1 | 2 | 3;
    /** TeamWithMembers */
    TeamWithMembers: {
      /** Name */
      name: string;
      /** Slogan */
      slogan: string | null;
      /** @default 2 */
      visibility?: components["schemas"]["TeamVisibility"];
      /** Active Until */
      active_until: string | null;
      /** Id */
      id: number;
      /** Active */
      active: boolean;
      /**
       * Created At
       * Format: date-time
       */
      created_at: string;
      /**
       * Updated At
       * Format: date-time
       */
      updated_at: string;
      /** User Links */
      user_links: components["schemas"]["TeamUserLinkPublic"][];
    };
    /** User */
    User: {
      /** Username */
      username: string;
      /** Email */
      email: string;
      /**
       * Country
       * @default XX
       */
      country?: string;
      /** Id */
      id?: number | null;
      /** Hashed Password */
      hashed_password: string;
      /** @default 1 */
      privileges?: components["schemas"]["UserPriv"];
      /**
       * Created At
       * Format: date-time
       */
      created_at?: string;
      /**
       * Updated At
       * Format: date-time
       */
      updated_at?: string;
    };
    /**
     * UserPriv
     * @enum {integer}
     */
    UserPriv: 1 | 2;
    /** UserRead */
    UserRead: {
      /** Username */
      username: string;
      /** Email */
      email: string;
      /**
       * Country
       * @default XX
       */
      country?: string;
      /** Id */
      id: number;
      privileges: components["schemas"]["UserPriv"];
    };
    /** UserUpdate */
    UserUpdate: {
      /** Password */
      password: string | null;
      /** Email */
      email: string | null;
      /** Username */
      username: string | null;
      /** Country */
      country: string | null;
    };
    /** UserWrite */
    UserWrite: {
      /** Username */
      username: string;
      /** Email */
      email: string;
      /**
       * Country
       * @default XX
       */
      country?: string;
      /** Password */
      password: string;
    };
    /** ValidationError */
    ValidationError: {
      /** Location */
      loc: (string | number)[];
      /** Message */
      msg: string;
      /** Error Type */
      type: string;
    };
    /**
     * WinCondition
     * @enum {integer}
     */
    WinCondition: 1 | 2 | 3 | 4;
  };
  responses: never;
  parameters: never;
  requestBodies: never;
  headers: never;
  pathItems: never;
}

export type $defs = Record<string, never>;

export type external = Record<string, never>;

export interface operations {

  /** Root */
  root__get: {
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": unknown;
        };
      };
    };
  };
  /** Users:Current User */
  users_current_user_users_me_get: {
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["User"];
        };
      };
    };
  };
  /** Users:Patch Current User */
  users_patch_current_user_users_me_patch: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["UserUpdate"];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["User"];
        };
      };
    };
  };
  /** Users:User */
  users_user_users__id__get: {
    parameters: {
      path: {
        id: string;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["User"];
        };
      };
    };
  };
  /** Users:Delete User */
  users_delete_user_users__id__delete: {
    parameters: {
      path: {
        id: string;
      };
    };
    responses: {
      /** @description Successful Response */
      204: {
        content: never;
      };
    };
  };
  /** Users:Patch User */
  users_patch_user_users__id__patch: {
    parameters: {
      path: {
        id: string;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["UserUpdate"];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["User"];
        };
      };
    };
  };
  /** Auth:Jwt.Login */
  auth_jwt_login_auth_jwt_login_post: {
    requestBody: {
      content: {
        "application/x-www-form-urlencoded": components["schemas"]["Body_auth_jwt_login_auth_jwt_login_post"];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["BearerResponse"];
        };
      };
    };
  };
  /** Auth:Jwt.Logout */
  auth_jwt_logout_auth_jwt_logout_post: {
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": unknown;
        };
      };
    };
  };
  /** Register:Register */
  register_register_auth_register_post: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["UserWrite"];
      };
    };
    responses: {
      /** @description Successful Response */
      201: {
        content: {
          "application/json": components["schemas"]["UserRead"];
        };
      };
    };
  };
  /** Get Score */
  get_score_scores__score_id__get: {
    parameters: {
      path: {
        score_id: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Score"];
        };
      };
    };
  };
  /** Submit Score */
  submit_score_scores__post: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["ScoreBase"];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Score"];
        };
      };
    };
  };
  /** Submit Score Partial */
  submit_score_partial_scores_partial__post: {
    parameters: {
      query: {
        keywords: string;
        beatmap_md5: string;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Score"];
        };
      };
    };
  };
  /** Inspect Bancho Match */
  inspect_bancho_match_scores_inspect_bancho__match_id__post: {
    parameters: {
      path: {
        match_id: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": unknown;
        };
      };
    };
  };
  /** Get Beatmap */
  get_beatmap_beatmaps__ident__get: {
    parameters: {
      path: {
        ident: string;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Beatmap"];
        };
      };
    };
  };
  /** Stream Beatmap */
  stream_beatmap_beatmaps_stream__post: {
    requestBody: {
      content: {
        "application/json": string[];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": unknown;
        };
      };
    };
  };
  /** Get Teams */
  get_teams_teams__get: {
    parameters: {
      query?: {
        limit?: number;
        offset?: number;
        active_only?: boolean;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["TeamWithMembers"][];
        };
      };
    };
  };
  /** Get Team */
  get_team_teams__team_id__get: {
    parameters: {
      path: {
        team_id: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Team"] | null;
        };
      };
    };
  };
  /** Create Team */
  create_team_teams__team_id__post: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["TeamBase"];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Team"] | null;
        };
      };
    };
  };
  /** Patch Team */
  patch_team_teams__team_id__patch: {
    parameters: {
      path: {
        team_id: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["TeamBase"];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Team"] | null;
        };
      };
    };
  };
  /** Get Teams Me */
  get_teams_me_teams_me__get: {
    parameters: {
      query?: {
        limit?: number;
        offset?: number;
        active_only?: boolean;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["TeamWithMembers"][];
        };
      };
    };
  };
  /** Get Scores */
  get_scores_teams_scores__get: {
    parameters: {
      query: {
        limit?: number;
        offset?: number;
        team_id: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Score"][];
        };
      };
    };
  };
  /** Get Stages */
  get_stages_teams_stages__get: {
    parameters: {
      query: {
        limit?: number;
        offset?: number;
        team_id: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Stage"][];
        };
      };
    };
  };
  /** Get Stage */
  get_stage_stages__stage_id__get: {
    parameters: {
      path: {
        stage_id: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Stage"];
        };
      };
    };
  };
  /** Patch Stage */
  patch_stage_stages__stage_id__patch: {
    parameters: {
      path: {
        stage_id: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["StageUpdate"];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Stage"];
        };
      };
    };
  };
  /** Create Stage */
  create_stage_stages__post: {
    parameters: {
      query: {
        team_id: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["StageBase"];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Stage"];
        };
      };
    };
  };
  /** Get Stage Beatmaps */
  get_stage_beatmaps_stages_beatmaps__get: {
    parameters: {
      query: {
        limit?: unknown;
        offset?: unknown;
        stage_id: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Beatmap"][];
        };
      };
    };
  };
  /** Add Stage Beatmaps */
  add_stage_beatmaps_stages_beatmaps__post: {
    parameters: {
      query: {
        stage_id: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["StageMapBase"][];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": unknown;
        };
      };
    };
  };
  /** Process Bancho Oauth */
  process_bancho_oauth_oauth_bancho_token_get: {
    parameters: {
      query: {
        code: string;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": unknown;
        };
      };
    };
  };
}
